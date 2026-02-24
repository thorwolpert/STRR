def test_setup_check(session, setup_parents):
    """Simple test to ensure the DB and TestContainers are setup correctly."""

    user_id = setup_parents["user_id"]

    assert user_id
    assert setup_parents["customer_id"]
    assert setup_parents["application_id"]
    assert setup_parents["registration_id"]
