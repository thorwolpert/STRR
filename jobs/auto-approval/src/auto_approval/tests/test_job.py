import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

from auto_approval.job import (create_app, get_bearer_token,
                               register_shellcontext, run)


class TestAutoApprovalJob(unittest.TestCase):

    @patch("auto_approval.job.create_app")
    @patch("auto_approval.job.Application")
    @patch("auto_approval.job.ApprovalService")
    @patch("auto_approval.job.get_bearer_token")
    @patch("auto_approval.job.datetime")
    def test_run_processes_eligible_applications(
        self,
        mock_datetime,
        mock_get_bearer_token,
        mock_approval_service,
        mock_application,
        mock_create_app,
    ):
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_now = datetime(2024, 8, 6, 16, 41, 31, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now
        mock_datetime.timedelta.side_effect = lambda **kwargs: timedelta(**kwargs)
        mock_application.application_date = MagicMock()
        mock_application.application_date.__le__.return_value = True
        mock_application.Status = MagicMock()
        mock_application.Status.SUBMITTED = "SUBMITTED"
        mock_application_instance1 = MagicMock()
        mock_application_instance1.id = 1
        mock_application_instance1.application_date = mock_now - timedelta(hours=2)
        mock_application_instance1.status = "SUBMITTED"
        mock_application_instance2 = MagicMock()
        mock_application_instance2.id = 2
        mock_application_instance2.application_date = mock_now - timedelta(hours=3)
        mock_application_instance2.status = "SUBMITTED"
        mock_application.query.filter.return_value.all.return_value = [
            mock_application_instance1,
            mock_application_instance2,
        ]
        mock_token = {"access_token": "test_token"}
        mock_get_bearer_token.return_value = mock_token
        run()
        mock_create_app.assert_called_once()
        mock_application.query.filter.assert_called_once()
        filter_args = mock_application.query.filter.call_args[0]
        self.assertEqual(len(filter_args), 2)
        self.assertTrue(mock_application.application_date.__le__.called)
        self.assertEqual(filter_args[1], mock_application.status == "SUBMITTED")

        self.assertEqual(
            mock_approval_service.process_auto_approval.call_count,
            2,
            "process_auto_approval should be called twice, once for each application",
        )

        calls = mock_approval_service.process_auto_approval.call_args_list
        self.assertEqual(len(calls), 2, "process_auto_approval should be called twice")
        for call, mock_instance in zip(
            calls, [mock_application_instance1, mock_application_instance2]
        ):
            args, kwargs = call
            self.assertEqual(
                kwargs["token"], mock_token, "token should match the mock token"
            )
            self.assertEqual(
                kwargs["application"],
                mock_instance,
                "application passed to process_auto_approval should match the mock instance",
            )

        mock_app.logger.info.assert_any_call("Auto processing application 1")
        mock_app.logger.info.assert_any_call("Auto processing application 2")

    @patch("auto_approval.job.create_app")
    @patch("auto_approval.job.Application")
    @patch("auto_approval.job.ApprovalService")
    @patch("auto_approval.job.get_bearer_token")
    @patch("auto_approval.job.datetime")
    def test_run_handles_no_eligible_applications(
        self,
        mock_datetime,
        mock_get_bearer_token,
        mock_approval_service,
        mock_application,
        mock_create_app,
    ):
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_now = datetime(2024, 8, 6, 16, 41, 31, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now
        mock_datetime.timedelta.side_effect = lambda **kwargs: timedelta(**kwargs)
        mock_application.application_date = MagicMock()
        mock_application.application_date.__le__.return_value = True
        mock_application.Status = MagicMock()
        mock_application.Status.SUBMITTED = "SUBMITTED"
        mock_application.query.filter.return_value.all.return_value = []
        run()
        mock_create_app.assert_called_once()
        mock_application.query.filter.assert_called_once()
        filter_args = mock_application.query.filter.call_args[0]
        self.assertEqual(len(filter_args), 2)
        self.assertTrue(mock_application.application_date.__le__.called)
        self.assertEqual(filter_args[1], mock_application.status == "SUBMITTED")
        mock_approval_service.process_auto_approval.assert_not_called()
        mock_get_bearer_token.assert_not_called()

    @patch("auto_approval.job.create_app")
    @patch("auto_approval.job.Application")
    @patch("auto_approval.job.datetime")
    def test_run_logs_exception(self, mock_datetime, mock_application, mock_create_app):
        mock_app = MagicMock()
        mock_create_app.return_value = mock_app
        mock_now = datetime(2024, 8, 6, 16, 41, 31, tzinfo=timezone.utc)
        mock_datetime.now.return_value = mock_now
        mock_datetime.timedelta.side_effect = lambda **kwargs: timedelta(**kwargs)
        mock_application.query.filter.side_effect = Exception("Test exception")
        run()
        mock_create_app.assert_called_once()
        mock_app.logger.error.assert_called_once()

    @patch("auto_approval.job.Flask")
    @patch("auto_approval.job.CONFIGURATION")
    @patch("auto_approval.job.db")
    @patch("auto_approval.job.sentry_sdk")
    def test_create_app(self, mock_sentry_sdk, mock_db, mock_configuration, mock_flask):
        mock_app = MagicMock()
        mock_flask.return_value = mock_app
        mock_configuration.__getitem__.return_value = MagicMock()
        mock_app.config.__getitem__.return_value = "test_dsn"
        result = create_app()
        self.assertEqual(result, mock_app)
        mock_flask.assert_called_once_with("auto_approval.job")
        mock_app.config.from_object.assert_called_once()
        mock_db.init_app.assert_called_once_with(mock_app)
        mock_sentry_sdk.init.assert_called_once()

    def test_register_shellcontext(self):
        mock_app = MagicMock()
        register_shellcontext(mock_app)
        mock_app.shell_context_processor.assert_called_once()

    @patch("auto_approval.job.AuthService")
    def test_get_bearer_token(self, mock_auth_service):
        mock_token = {"access_token": "test_token"}
        mock_auth_service.get_service_client_token.return_value = mock_token
        result = get_bearer_token()
        self.assertEqual(result, mock_token)
        mock_auth_service.get_service_client_token.assert_called_once()
