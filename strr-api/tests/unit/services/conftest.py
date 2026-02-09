from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy.orm import Session

from strr_api.models import Application, Registration, User


@pytest.fixture
def setup_parents(session: Session, random_string, random_integer):
    """
    Creates one parent record in each table so we have valid IDs
    to link our interactions to.

    TODO: this should be part of a session wide set of fixture strategy
    """
    customer = User(id=random_integer())
    user = User(id=random_integer())
    reg = Registration(
        id=random_integer(),
        registration_type=Registration.RegistrationType.HOST,
        registration_number=random_string(10),
        sbc_account_id=random_integer(),
        status="ACTIVE",
        user_id=user.id,
        start_date=datetime.now(timezone.utc),
        expiry_date=(datetime.now(timezone.utc) + timedelta(days=365)).date(),
    )
    app = Application(
        id=random_integer(),
        application_json={},
        registration_id=reg.id,
        application_number=random_string(10),
        type="",
        registration_type=Registration.RegistrationType.HOST,
    )

    session.add_all([user, app, customer, reg])
    session.commit()

    return {
        "application_id": app.id,
        "customer_id": customer.id,
        "registration_id": reg.id,
        "user_id": user.id,
    }
