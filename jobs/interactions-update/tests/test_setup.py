def test_setup_check(db_session):
    """Simple test to ensure the DB and TestContainers are setup correctly."""

    from strr_api.models import User

    user = User()
    db_session.add(user)

    db_session.flush()

    assert user.id
