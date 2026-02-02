# Copyright © 2023 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""Common setup and fixtures for the pytest suite used by this service."""
import contextlib
import random
import string
from contextlib import contextmanager

import psycopg2
import pytest
import sqlalchemy
from flask_migrate import Migrate, upgrade
from ldclient.integrations.test_data import TestData
from sqlalchemy import event, text
from sqlalchemy.orm import Session as AppSession
from testcontainers.postgres import PostgresContainer

from strr_api import create_app
from strr_api import db as _db
from strr_api import jwt as _jwt
from strr_api.config import Testing

postgres_image = "postgres:16-alpine"


@pytest.fixture(scope="function")
def random_string():
    """Returns a random string, defult length is 10."""
    def _generate(length=10):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters, k=length))
    
    return _generate


@contextmanager
def not_raises(exception):
    """Corallary to the pytest raises builtin.

    Assures that an exception is NOT thrown.
    """
    try:
        yield
    except exception:
        raise pytest.fail(f"DID RAISE {exception}")


@pytest.fixture(scope="session")
def ld():
    """LaunchDarkly TestData source."""
    td = TestData.data_source()
    yield td


@pytest.fixture(scope="session")
def client(app):  # pylint: disable=redefined-outer-name
    """Return a session-wide Flask test client."""
    return app.test_client()


@pytest.fixture(scope="session")
def jwt():
    """Return a session-wide jwt manager."""
    return _jwt


@pytest.fixture(scope="session")
def client_ctx(app):  # pylint: disable=redefined-outer-name
    """Return session-wide Flask test client."""
    with app.test_client() as _client:
        yield _client


@pytest.fixture(scope="session")
def postgres_container():
    """
    Spins up a Postgres container.
    """
    with PostgresContainer(postgres_image) as postgres:
        yield postgres

@pytest.fixture(scope="session")
def app(ld, postgres_container):
    """
    Creates the Flask application using the container's credentials.
    """
    db_url = postgres_container.get_connection_url()
    Testing.SQLALCHEMY_DATABASE_URI= db_url
    # This makes sure that the app is configured and doesn't skip setup steps
    Testing.POD_NAMESPACE = 'Testing'
    
    app = create_app(Testing, **{"ld_test_data": ld})
    
    with app.app_context():
        yield app

@pytest.fixture(scope="session")
def setup_database(app):
    """
    Applies database migrations to the test container.
    Replaces db.create_all() with flask_migrate.upgrade()
    """
    # This applies all migrations up to 'head'
    # It assumes your 'migrations' folder is in the project root
    upgrade()
    
    yield
    

@pytest.fixture(scope="function")
def session(app, setup_database):
    """
    Creates a test session that behaves like a scoped_session but
    is bound to an external transaction for easy rollback.
    """
    # 1. Start the external transaction on the connection
    connection = _db.engine.connect()
    transaction = connection.begin()

    # 2. Create the Session
    # join_transaction_mode="create_savepoint":
    # This ensures that when your app calls session.commit(), it creates a 
    # nested SAVEPOINT (which we can rollback) instead of committing the real transaction.
    session = AppSession(bind=connection, join_transaction_mode="create_savepoint")

    # 3. Create a Proxy to mimic Flask-SQLAlchemy's db.session
    # This class ensures that both `db.session.add()` and `db.session()` work.
    class TestScopedSession:
        def __call__(self):
            # Allows calling db.session() to get the current session
            return session
        
        def __getattr__(self, name):
            # Proxies attributes like .add, .query, .commit to the session
            return getattr(session, name)
            
        def remove(self):
            # Safe no-op or close
            session.close()

    # 4. Patch global db.session
    original_session_lookup = _db.session
    _db.session = TestScopedSession()

    yield session

    # 5. Cleanup
    _db.session = original_session_lookup  # Restore global registry
    session.close()
    
    # Force rollback of the external transaction (wiping all test data)
    transaction.rollback()
    connection.close()
