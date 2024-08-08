# Copyright © 2024 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Auto Approval Job."""
import logging
import os
import time
from datetime import datetime, timedelta, timezone

import sentry_sdk
from flask import Flask
from pg8000.dbapi import ProgrammingError
from sentry_sdk.integrations.logging import LoggingIntegration
from sqlalchemy.exc import SQLAlchemyError
from strr_api.models import db
from strr_api.models.application import Application
from strr_api.services import ApprovalService, AuthService

from auto_approval.config import CONFIGURATION
from auto_approval.utils.logging import setup_logging

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), "logging.conf"))

SENTRY_LOGGING = LoggingIntegration(event_level=logging.ERROR)  # send errors as events


def create_app(run_mode=os.getenv("FLASK_ENV", "production")):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app_config = CONFIGURATION[run_mode]
    app.config.from_object(app_config)
    db.init_app(app)
    # Configure Sentry
    if app.config.get("SENTRY_DSN", None):
        sentry_sdk.init(dsn=app.config.get("SENTRY_DSN"), integrations=[SENTRY_LOGGING])
    register_shellcontext(app)
    app.logger.info(
        f"AUTO_APPROVAL_MIN_APPLICATION_SUBMITTED_MINUTES={str(app.config.get("AUTO_APPROVAL_MIN_APPLICATION_SUBMITTED_MINUTES"))}"
    )
    return app


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"app": app}

    app.shell_context_processor(shell_context)


def get_submitted_applications(app):
    """Retrieve submitted applications for processing."""
    time_delta = timedelta(
        minutes=app.config.get("AUTO_APPROVAL_MIN_APPLICATION_SUBMITTED_MINUTES")
    )
    cutoff_time = datetime.now(timezone.utc) - time_delta
    return Application.query.filter(
        Application.application_date <= cutoff_time,
        Application.status == Application.Status.SUBMITTED,
    ).all()


def process_applications(app, applications):
    """Process auto-approval for submitted applications."""
    token = AuthService.get_service_client_token()
    for application in applications:
        app.logger.info(f"Auto processing application {str(application.id)}")
        ApprovalService.process_auto_approval(token=token, application=application)


def run(max_attempts=5, max_delay=240):
    """Run the auto-approval job with retries."""
    app = create_app()
    for attempt in range(max_attempts):
        with app.app_context():
            try:
                applications = get_submitted_applications(app)
                process_applications(app, applications)
                return
            except (SQLAlchemyError, ProgrammingError) as e:
                if attempt < max_attempts - 1:
                    delay = min(max_delay, (2**attempt))
                    app.logger.warning(
                        f"Database error. Retrying in {delay}s. Error: {str(e)}"
                    )
                    time.sleep(delay)
                else:
                    app.logger.error(f"Max attempts reached. Job failed: {str(e)}")
            except Exception as err:
                app.logger.error(f"Unexpected error: {str(err)}")
                break
