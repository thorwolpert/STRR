# Copyright © 2024 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Enum definitions."""

from enum import Enum


class AuthHeaderType(Enum):
    """Authorization header types."""

    BASIC = "Basic {}"
    BEARER = "Bearer {}"


class ContentType(Enum):
    """Http Content Types."""

    JSON = "application/json"
    FORM_URL_ENCODED = "application/x-www-form-urlencoded"
    PDF = "application/pdf"


class LoginSource(Enum):
    """Login source values."""

    PASSCODE = "PASSCODE"
    BCSC = "BCSC"
    BCEID = "BCEID"
    STAFF = "IDIR"
    BCROS = "BCROS"
    API_GW = "API_GW"
    IDIR = "IDIR"


class Role(Enum):
    """User Role."""

    VIEWER = "view"
    EDITOR = "edit"
    PUBLIC_USER = "public_user"
    ACCOUNT_HOLDER = "account_holder"
    GOV_ACCOUNT_USER = "gov_account_user"
    ANONYMOUS_USER = "anonymous_user"
    ACCOUNT_IDENTITY = "account_identity"
    MANAGE_EFT = "manage_eft"

    SYSTEM = "system"
    TESTER = "tester"

    STAFF = "staff"
    STAFF_VIEW_ACCOUNTS = "view_accounts"
    STAFF_MANAGE_ACCOUNTS = "manage_accounts"
    STAFF_SEARCH = "search"
    STAFF_CREATE_ACCOUNTS = "create_accounts"
    STAFF_MANAGE_BUSINESS = "manage_business"
    STAFF_SUSPEND_ACCOUNTS = "suspend_accounts"

    STRR_EXAMINER = "strr_examiner"
    STRR_INVESTIGATOR = "strr_investigator"
    STRR_AUTOMATION_TESTER = "strr_automation_tester"


class RegistrationStatus(Enum):
    """STRR Registration Status."""

    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"


class RegistrationSortBy(Enum):
    """STRR Registration Sort By Columns."""

    ID = 0
    REGISTRATION_NUMBER = 1
    LOCATION = 2
    ADDRESS = 3
    NAME = 4
    STATUS = 5
    SUBMISSION_DATE = 6


class PropertyType(Enum):
    """STRR Property Type."""

    SINGLE_FAMILY_HOME = "Single Family Home"
    SECONDARY_SUITE = "Secondary suite"
    ACCESSORY_DWELLING = "Accessory dwelling unit"
    MULTI_UNIT_HOUSING = "Small scale, multi-unit housing"
    TOWN_HOME = "Town Home"
    CONDO_OR_APT = "Condo or Apartment"
    RECREATIONAL = "Recreational Property"
    BED_AND_BREAKFAST = "Bed and Breakfast"
    STRATA_HOTEL = "Strata Hotel"
    FLOAT_HOME = "Float home"


class PaymentStatus(Enum):
    """Payment status codes."""

    CREATED = "CREATED"
    COMPLETED = "COMPLETED"
    PAID = "PAID"
    APPROVED = "APPROVED"
    DELETED = "DELETED"
    REFUNDED = "REFUNDED"
    FAILED = "FAILED"


class ApplicationType(Enum):
    """STRR Application Types."""

    REGISTRATION = "registration"


class RegistrationType(Enum):
    """STRR Registration Types."""

    HOST = "HOST"
    PLATFORM = "PLATFORM"
    STRATA_HOTEL = "STRATA_HOTEL"


class ErrorMessage(Enum):
    """STRR Error Messages."""

    APPLICATION_NOT_FOUND = "Application not found."
    INVALID_APPLICATION_STATUS = "Invalid application status."
    APPLICATION_TERMINAL_STATE = "Application has reached the final state."
    PROCESSING_ERROR = "An error occurred while processing the request."
    DOCUMENT_NOT_FOUND = "Document not found."
    APPLICATION_NOT_PAID = "Application does not have a payment record."
    REGISTRATION_NOT_FOUND = "Application not found."
    PLATFORM_ISSUE_CERTIFICATE_ERROR = "Certificate is not available for a platform registration."
    INVOICE_CREATION_ERROR = "Error while creating invoice."
    APPLICATION_NOT_MODIFIABLE = "Application cannot be modified."
    ADDRESS_NOT_FOUND = "Address not found."


class ApplicationRole(Enum):
    """STRR Application Roles."""

    HOST = "HOST"
