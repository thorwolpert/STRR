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
from datetime import datetime, timedelta, timezone

import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.logging import LoggingIntegration
from strr_api.models.application import Application
from strr_api.models.user import User
from strr_api.services import ApprovalService

from auto_approval.config import CONFIGURATION
from auto_approval.utils.logging import setup_logging

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), "logging.conf"))

SENTRY_LOGGING = LoggingIntegration(event_level=logging.ERROR)  # send errors as events


def create_app(run_mode=os.getenv("FLASK_ENV", "production")):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.config.from_object(CONFIGURATION[run_mode])
    db.init_app(app)
    # Configure Sentry
    if app.config.get("SENTRY_DSN", None):
        sentry_sdk.init(dsn=app.config.get("SENTRY_DSN"), integrations=[SENTRY_LOGGING])

    register_shellcontext(app)

    return app


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"app": app}

    app.shell_context_processor(shell_context)


def create_jwt_token_from_user(user: User) -> dict:
    """Create a JWT token dict from a User object."""
    JWT_OIDC_USERNAME = os.getenv("JWT_OIDC_USERNAME", "username")
    JWT_OIDC_FIRSTNAME = os.getenv("JWT_OIDC_FIRSTNAME", "firstname")
    JWT_OIDC_LASTNAME = os.getenv("JWT_OIDC_LASTNAME", "lastname")

    token = {
        "sub": user.sub,
        "iss": user.iss,
        "idp_userid": user.idp_userid,
        "loginSource": user.login_source,
        JWT_OIDC_USERNAME: user.username,
        JWT_OIDC_FIRSTNAME: user.firstname,
        JWT_OIDC_LASTNAME: user.lastname,
    }

    return token


def run():
    """Applies auto approval logic against STRR applications and updates the application status."""
    application = create_app()
    with application.app_context():
        try:
            one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
            applications = Application.query.filter(
                Application.application_date <= one_hour_ago,
                Application.status == Application.Status.SUBMITTED,
            ).all()

            for application in applications:
                submitter = application.submitter
                token = create_jwt_token_from_user(user=submitter)
                ApprovalService.process_auto_approval(
                    token=token, application=application
                )
        except Exception as err:
            application.logger.error(err)
