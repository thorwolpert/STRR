# Copyright © 2024 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Manages filing type codes and payment service interactions."""
from http import HTTPStatus

import requests
from flask import Flask
from flask_jwt_oidc import JwtManager

from strr_api.enums.enum import RegistrationType
from strr_api.exceptions import ExternalServiceException
from strr_api.models import Application, Events
from strr_api.services.events_service import EventsService
from strr_api.services.user_service import UserService

PLATFORM_SMALL_USER_BASE = "PLATREG_SM"

PLATFORM_LARGE_USER_BASE = "PLATREG_LG"

PLATFORM_FEE_WAIVED = "PLATREG_WV"


class PayService:
    """
    A class that provides utility functions for connecting with the BC Registries pay-api.
    """

    app: Flask = None
    default_invoice_payload: dict = {}
    svc_url: str = None
    timeout: int = None

    def __init__(self, app: Flask = None):
        """Initialize the pay service."""
        if app:
            self.init_app(app)

    def init_app(self, app: Flask):
        """Initialize app dependent variables."""
        self.app = app
        self.svc_url = app.config.get("PAYMENT_SVC_URL")
        self.timeout = app.config.get("PAY_API_TIMEOUT", 20)

    def create_invoice(self, user_jwt: JwtManager, account_id, application=None):
        """Create the invoice via the pay-api."""
        application_json = application.application_json
        payload = self._get_payment_request(application_json)
        try:
            token = user_jwt.get_token_auth_header()
            headers = {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
                "Account-Id": str(account_id),
            }
            resp = requests.post(
                url=self.svc_url + "/payment-requests", json=payload, headers=headers, timeout=self.timeout
            )

            if resp.status_code not in [HTTPStatus.OK, HTTPStatus.CREATED] or not (resp.json()).get("id", None):
                error = f"{resp.status_code} - {str(resp.json())}"
                self.app.logger.debug("Invalid response from pay-api: %s", error)
                raise ExternalServiceException(error=error, status_code=HTTPStatus.PAYMENT_REQUIRED)

            EventsService.save_event(
                event_type=Events.EventType.APPLICATION,
                event_name=Events.EventName.INVOICE_GENERATED,
                application_id=application.id,
            )
            return resp.json()
        except ExternalServiceException as exc:
            # pass along
            raise exc
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as err:
            self.app.logger.debug("Pay-api connection failure:", repr(err))
            raise ExternalServiceException(error=repr(err), status_code=HTTPStatus.GATEWAY_TIMEOUT) from err
        except Exception as err:
            self.app.logger.debug("Pay-api integration (create invoice) failure:", repr(err))
            raise ExternalServiceException(error=repr(err), status_code=HTTPStatus.PAYMENT_REQUIRED) from err

    def _get_payment_request(self, application_json):
        filing_type = None
        registration_json = application_json.get("registration", {})
        registration_type = registration_json.get("registrationType")
        if registration_type == RegistrationType.HOST.value:
            filing_type = "RENTAL_FEE"
        if registration_type == RegistrationType.PLATFORM.value:
            cpbc_number = registration_json.get("businessDetails").get("consumerProtectionBCLicenceNumber")
            if cpbc_number and (not cpbc_number.isspace()):
                filing_type = PLATFORM_FEE_WAIVED
            elif registration_json.get("platformDetails").get("listingSize") == "GREATER_THAN_THOUSAND":
                filing_type = PLATFORM_LARGE_USER_BASE
            else:
                filing_type = PLATFORM_SMALL_USER_BASE

        filing_type_dict = {"filingTypeCode": filing_type}

        # Workaround to charge the service fee when the filing fee is 0.
        if filing_type == PLATFORM_FEE_WAIVED:
            filing_type_dict["fee"] = 0

        payload = {"filingInfo": {"filingTypes": [filing_type_dict]}, "businessInfo": {"corpType": "STRR"}}

        if registration_type == RegistrationType.HOST.value:
            payload["paymentInfo"] = {"methodOfPayment": "DIRECT_PAY"}

        if UserService.is_automation_tester():
            payload["skipPayment"] = True

        return payload

    def get_payment_details_by_invoice_id(self, user_jwt: JwtManager, account_id, invoice_id: int):
        """Get payment details by invoice id."""
        token = user_jwt.get_token_auth_header()
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Account-Id": str(account_id),
        }
        payment_details = requests.get(
            url=self.svc_url + f"/payment-requests/{invoice_id}", headers=headers, timeout=self.timeout
        ).json()
        return payment_details

    def get_payment_receipt(self, user_jwt: JwtManager, application: Application):
        """Gets the payment receipt of an application."""
        token = user_jwt.get_token_auth_header()
        url = f"{self.svc_url}/payment-requests/{application.invoice_id}/receipts"
        headers = {
            "Accept": "application/pdf",
            "Authorization": f"Bearer {token}",
            "Account-Id": str(application.payment_account),
        }
        payload = {
            "filingDateTime": application.application_date.isoformat(),
            "effectiveDateTime": "",
            "filingIdentifier": str(application.id),
        }
        response = requests.post(
            url,
            json=payload,
            headers=headers,
        )
        if response.status_code != HTTPStatus.CREATED:
            self.app.logger.error("Failed to get receipt pdf for filing: %s", application.id)

        return self.app.response_class(
            response=response.content,
            status=response.status_code,
            mimetype="application/pdf",
        )
