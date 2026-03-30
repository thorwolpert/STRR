"""Registration Renewal Reminder Job."""

from datetime import datetime
from datetime import timedelta
from datetime import timezone
import logging
import os
import traceback

from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import exists
from sqlalchemy import func
from strr_api.enums.enum import ApplicationType
from strr_api.enums.enum import RegistrationStatus
from strr_api.models import CustomerInteraction
from strr_api.models import db
from strr_api.models.application import Application
from strr_api.models.rental import Registration
from strr_api.services.email_service import EmailService
from strr_api.services.events_service import Events
from strr_api.services.events_service import EventsService

from renewal_reminders.config import _Config
from renewal_reminders.config import CONFIGURATION
from renewal_reminders.utils.logging import setup_logging

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), "logging.conf"))


def create_app(run: str | _Config = "production", **kwargs):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)

    if not isinstance(run, str) and issubclass(run, _Config):
        config = run
    else:
        config = CONFIGURATION[run]

    app.config.from_object(config)
    db.init_app(app)
    if app.config.get("POD_NAMESPACE", None) == "Testing":
        Migrate(app, db)

    register_shellcontext(app)
    return app


def register_shellcontext(app):
    """Register shell context objects."""

    def shell_context():
        """Shell context objects."""
        return {"app": app}

    app.shell_context_processor(shell_context)
