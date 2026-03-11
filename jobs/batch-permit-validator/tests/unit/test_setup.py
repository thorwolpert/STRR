def test_setup_check(session):
    """Simple test to ensure the DB and TestContainers are setup correctly."""

    from strr_api.models import User

    user = User()
    session.add(user)

    session.commit()
