from unittest.mock import MagicMock, patch

import pytest
from strr_api.models.application import Application
from strr_api.models.user import User

from auto_approval.job import create_app, create_jwt_token_from_user, run


@pytest.fixture
def mock_app():
    app = MagicMock()
    app.config = {"SENTRY_DSN": "test_dsn"}
    return app


@pytest.fixture
def mock_db():
    with patch("auto_approval.job.db") as mock:
        yield mock


@pytest.fixture
def mock_sentry():
    with patch("auto_approval.job.sentry_sdk") as mock:
        yield mock


def test_create_app(mock_db, mock_sentry):
    with patch("auto_approval.job.Flask") as mock_flask:
        mock_flask.return_value = mock_app()
        app = create_app()

        assert app is not None
        mock_flask.assert_called_once_with(__name__)
        mock_db.init_app.assert_called_once()
        mock_sentry.init.assert_called_once()


def test_create_jwt_token_from_user():
    user = User(
        sub="test_sub",
        iss="test_iss",
        idp_userid="test_idp_userid",
        login_source="test_login_source",
        username="test_username",
        firstname="Test",
        lastname="User",
    )

    token = create_jwt_token_from_user(user)

    assert token["sub"] == "test_sub"
    assert token["iss"] == "test_iss"
    assert token["idp_userid"] == "test_idp_userid"
    assert token["loginSource"] == "test_login_source"
    assert token["username"] == "test_username"
    assert token["firstname"] == "Test"
    assert token["lastname"] == "User"


@pytest.fixture
def mock_applications():
    return [MagicMock(spec=Application) for _ in range(3)]


@pytest.fixture
def mock_users():
    return [MagicMock(spec=User) for _ in range(3)]


@patch("auto_approval.job.create_app")
@patch("auto_approval.job.Application")
@patch("auto_approval.job.ApprovalService")
@patch("auto_approval.job.create_jwt_token_from_user")
def test_run(
    mock_create_jwt_token,
    mock_approval_service,
    mock_application_model,
    mock_create_app,
    mock_applications,
    mock_users,
):
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app

    # Set up the mock applications and users
    for app, user in zip(mock_applications, mock_users):
        app.submitter = user

    # Mock the query filter to return our mock applications
    mock_application_model.query.filter.return_value.filter.return_value.all.return_value = (
        mock_applications
    )

    # Run the function
    run()

    # Assertions
    mock_create_app.assert_called_once()
    mock_app.app_context.assert_called_once()

    # Check that the filter was called with the correct arguments
    mock_application_model.query.filter.assert_called_once()
    filter_call = mock_application_model.query.filter.call_args[0][0]
    assert str(filter_call) == "application_date <= :application_date_1"

    # Check that the second filter (for status) was called
    mock_application_model.query.filter.return_value.filter.assert_called_once_with(
        Application.status == Application.Status.SUBMITTED
    )

    # Check that create_jwt_token_from_user was called for each application
    assert mock_create_jwt_token.call_count == len(mock_applications)
    for i, app in enumerate(mock_applications):
        assert mock_create_jwt_token.call_args_list[i][0][0] == app.submitter

    # Check that process_auto_approval was called for each application
    assert mock_approval_service.process_auto_approval.call_count == len(
        mock_applications
    )

    # Check that each call to process_auto_approval used the correct application and a token created from its submitter
    for i, app in enumerate(mock_applications):
        call_args = mock_approval_service.process_auto_approval.call_args_list[i]
        assert call_args[1]["application"] == app
        assert isinstance(call_args[1]["token"], dict)
        assert call_args[1]["token"] == mock_create_jwt_token.return_value


@patch("auto_approval.job.create_app")
@patch("auto_approval.job.Application")
def test_run_with_exception(mock_application_model, mock_create_app):
    mock_app = MagicMock()
    mock_create_app.return_value = mock_app

    mock_application_model.query.filter.side_effect = Exception("Test exception")

    run()

    mock_create_app.assert_called_once()
    mock_app.app_context.assert_called_once()
    mock_app.logger.error.assert_called_once()
