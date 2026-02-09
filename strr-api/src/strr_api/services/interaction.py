import uuid
from dataclasses import dataclass
from http import HTTPStatus
from typing import overload

import requests
from flask import current_app, jsonify

from strr_api.exceptions import ExternalServiceException, ValidationException
from strr_api.models import CustomerInteraction, Events
from strr_api.services import AuthService
from strr_api.services.events_service import EventsService
from strr_api.utils.validate_calls import validate_mutex


@dataclass
class EmailInfo:
    """Email Info class"""

    application_number: str | None = None
    email_type: str | None = None
    custom_content: str | None = None
    registration_number: str | None = None


class InteractionService:
    """Service to handle interaction logic."""

    email_event_mapper = {
        "RENEWAL_REMINDER": Events.EventName.RENEWAL_REMINDER_SENT,
    }

    @overload
    def dispatch(*, application_id: int) -> None:
        ...

    @overload
    def dispatch(*, registration_id: int) -> None:
        ...

    @overload
    def dispatch(*, customer_id: int) -> None:
        ...

    @staticmethod
    @validate_mutex("application_id", "registration_id", "customer_id", min_count=1, max_count=1)
    def dispatch(
        channel_type: CustomerInteraction.ChannelType,
        payload: dict | str | EmailInfo,
        idempotency_key: str | None = None,
        user_id: int | None = None,
        application_id: int | None = None,
        registration_id: int | None = None,
        customer_id: int | None = None,
    ):
        """Dispatch interaction."""
        match channel_type:
            case CustomerInteraction.ChannelType.EMAIL:
                if not isinstance(payload, EmailInfo):
                    raise ValidationException(error="Invalid EmailInfo", status_code=HTTPStatus.BAD_REQUEST)
                notify_reference = InteractionService._send_email_to_notify_service(payload)

            case _:
                raise ExternalServiceException(error="Unsupported channel type", status_code=HTTPStatus.BAD_REQUEST)

        if (
            not notify_reference
            or not isinstance(notify_reference, dict)
            or not (notify_id := notify_reference.get("id"))
            or (notify_id < 1)
        ):
            raise ExternalServiceException(error="Email not sent", status_code=HTTPStatus.BAD_REQUEST)

        interaction = CustomerInteraction(
            channel=channel_type,
            application_id=application_id,
            registration_id=registration_id,
            customer_id=customer_id,
            user_id=user_id,
            notify_reference=notify_id,
            interaction_uuid=str(uuid.uuid4()),
        )
        interaction.save()

        event_type = (
            Events.EventType.REGISTRATION
            if registration_id
            else Events.EventType.APPLICATION
            if application_id
            else Events.EventType.USER
        )
        event_name = InteractionService.email_event_mapper[payload.email_type]

        EventsService.save_event(
            event_type=event_type,
            event_name=event_name,
            details=f"Interaction sent via {channel_type.value}",
            application_id=application_id,
            registration_id=registration_id,
            user_id=user_id,
        )

        return interaction

    @staticmethod
    def _send_email_to_notify_service(email: str):
        token = AuthService.get_service_client_token()
        try:
            resp = requests.post(
                current_app.config["NOTIFY_SVC_URL"],
                json=email,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
                timeout=current_app.config["NOTIFY_API_TIMEOUT"],
            )
        except Exception as err:
            current_app.logger.error(f"Email error, {err}")
            return {"id": -1}

        if resp.status_code not in [HTTPStatus.OK, HTTPStatus.ACCEPTED, HTTPStatus.CREATED]:
            current_app.logger.info(f"Error {resp.status_code} - {str(resp.json())}")
            return {"id": -1}

        return resp.json()
