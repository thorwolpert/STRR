import json
import os

from strr_api.enums.enum import OwnershipType, PaymentStatus, PropertyType, RegistrationStatus
from strr_api.exceptions import ExternalServiceException
from strr_api.models import (
    Address,
    Application,
    Contact,
    Document,
    Eligibility,
    Invoice,
    PropertyManager,
    Registration,
    RentalProperty,
    User,
)

from ..resources.test_registration_applications import CREATE_REGISTRATION_REQUEST


def mock_json_file(filename):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), f"../../mocks/json/{filename}.json")


def disable_jwt_requires_auth(f):
    return f


def fake_get_token_auth_header(arg):
    return "fake_jwt_token"


def fake_user_from_token(arg):
    return User(
        firstname="First",
        lastname="last",
        email="test@test.test",
        idp_userid="ABCDEFG",
    )


def fake_examiner_from_token(arg):
    return User(
        firstname="First",
        lastname="last",
        email="test@test.test",
        idp_userid="ABCDEFG",
        login_source="IDIR",
    )


def fake_user_from_db(*args, **kwargs):
    return User(
        id=1,
        firstname="First",
        lastname="last",
        email="test@test.test",
        idp_userid="ABCDEFG",
    )


def fake_registration_pending(*args, **kwargs):
    return Registration(
        id=1,
        user_id=1,
        sbc_account_id=1000,
        status=RegistrationStatus.PENDING,
        submission_date="2021-01-01T00:00:00Z",
        updated_date="2021-01-01T00:00:00Z",
        eligibility=Eligibility(
            id=1,
            registration_id=1,
            is_principal_residence=True,
            agreed_to_rental_act=True,
            agreed_to_submit=True,
        ),
        rental_property=RentalProperty(
            id=1,
            property_type=PropertyType.PRIMARY,
            ownership_type=OwnershipType.OWN,
            address=Address(
                id=1,
                street_address="123 Fake St",
                country="CA",
                city="Victoria",
                province="BC",
                postal_code="V8V 8V8",
            ),
            property_manager=PropertyManager(
                id=1,
                primary_contact=Contact(
                    id=1,
                    firstname="First",
                    lastname="Last",
                    email="first.last@bc.gov.ca",
                    phone_number="123-456-7890",
                    date_of_birth="1970-01-01",
                    address=Address(
                        id=1,
                        street_address="123 Fake St",
                        country="CA",
                        city="Victoria",
                        province="BC",
                        postal_code="V8V 8V8",
                    ),
                ),
            ),
        ),
    )


def fake_application(*args, **kwargs):
    with open(CREATE_REGISTRATION_REQUEST) as f:
        json_data = json.load(f)
        return Application(
            id=1,
            application_json=json_data,
            type="registration",
        )


def fake_registration(*args, **kwargs):
    return Registration(
        id=1,
        user_id=1,
        sbc_account_id=1000,
        status=RegistrationStatus.APPROVED,
        submission_date="2021-01-01T00:00:00Z",
        updated_date="2021-01-01T00:00:00Z",
        eligibility=Eligibility(
            id=1,
            registration_id=1,
            is_principal_residence=True,
            agreed_to_rental_act=True,
            agreed_to_submit=True,
        ),
        rental_property=RentalProperty(
            id=1,
            property_type=PropertyType.PRIMARY,
            ownership_type=OwnershipType.OWN,
            address=Address(
                id=1,
                street_address="123 Fake St",
                country="CA",
                city="Victoria",
                province="BC",
                postal_code="V8V 8V8",
            ),
            property_manager=PropertyManager(
                id=1,
                primary_contact=Contact(
                    id=1,
                    firstname="First",
                    lastname="Last",
                    email="first.last@bc.gov.ca",
                    phone_number="123-456-7890",
                    date_of_birth="1970-01-01",
                    address=Address(
                        id=1,
                        street_address="123 Fake St",
                        country="CA",
                        city="Victoria",
                        province="BC",
                        postal_code="V8V 8V8",
                    ),
                ),
            ),
        ),
    )


def fake_invoice(*args, **kwargs):
    return Invoice(
        id=1,
        registration_id=1,
        invoice_id=1,
        payment_status_code=PaymentStatus.CREATED,
        payment_completion_date=None,
        payment_account="3299",
    )


def fake_invoice_details(*args, **kwargs):
    return {"statusCode": "COMPLETED"}


def fake_document(*args, **kwargs):
    return Document(
        id=1,
        eligibility_id=1,
        file_name="file_name",
        file_type="file_type",
        path="path",
        eligibility=Eligibility(id=1, registration_id=1),
    )


def keycloak_profile_json(*args, **kwargs):
    return {"keycloakGuid": "ecb1ef8f2fee443eb14a414321bbc1f2"}


def new_sbc_account(*args, **kwargs):
    return {"id": 1}


def no_op(*args, **kwargs):
    None


def throw_external_service_exception(*args, **kwargs):
    raise ExternalServiceException("Test exception")


def empty_json(*args, **kwargs):
    return {}
