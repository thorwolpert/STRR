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
"""This manages a User record that can be used in an audit trail.

Actual user data is kept in the OIDC and IDP services, this data is
here as a convenience for audit and db reporting.
"""
from __future__ import annotations

from datetime import datetime

from flask import current_app
from sql_versioning import Versioned
from sqlalchemy.orm import relationship

from ..utils.user_context import UserContext, user_context

from .db import db


class Contact(Versioned, db.Model):
    """Contact model for storing information about non-registered users."""

    __tablename__ = "contacts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(1000), nullable=False)
    lastname = db.Column(db.String(1000), nullable=False)
    middlename = db.Column(db.String(1000))
    address_id = db.Column(db.Integer, db.ForeignKey("addresses.id"), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    preferredname = db.Column(db.String, nullable=True)
    phone_extension = db.Column(db.String, nullable=True)
    phone_country_code = db.Column(db.String, nullable=True)
    fax_number = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    social_insurance_number = db.Column(db.String, nullable=True)
    business_number = db.Column(db.String, nullable=True)
    job_title = db.Column(db.String, nullable=True)

    address = relationship("Address", back_populates="contact")

    def full_name(self):
        """Return the full name of the contact."""
        return f"{self.firstname} {self.lastname}"


class User(db.Model):
    """Used to hold the audit information for a User of this service."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(1000), index=True)
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    middlename = db.Column(db.String(1000))
    email = db.Column(db.String(1024))
    sub = db.Column(db.String(36), unique=True)
    iss = db.Column(db.String(1024))
    idp_userid = db.Column(db.String(256), index=True)
    login_source = db.Column(db.String(200), nullable=True)
    creation_date = db.Column(db.DateTime(timezone=True), default=datetime.now)

    @property
    def display_name(self):
        """Display name of user; do not show sensitive data like BCSC username.

        If there is actual name info, return that; otherwise username.
        """
        if self.firstname or self.lastname or self.middlename:
            return " ".join(filter(None, [self.firstname, self.middlename, self.lastname])).strip()

        # parse off idir\ or @idir
        if self.username[:4] == "idir":
            return self.username[5:]
        if self.username[-4:] == "idir":
            return self.username[:-5]

        # do not show services card usernames
        if self.username[:4] == "bcsc":
            return None

        return self.username if self.username else None

    @classmethod
    def find_by_id(cls, submitter_id: int = None) -> User | None:
        """Return a User if they exist and match the provided submitter id."""
        return cls.query.filter_by(id=submitter_id).one_or_none()

    @classmethod
    def find_by_jwt_token(cls, token: dict) -> User | None:
        """Return a User if they exist and match the provided JWT."""
        if user_id := token.get("idp_userid"):
            return cls.query.filter_by(idp_userid=user_id).one_or_none()
        return None

    @classmethod
    def create_from_jwt_token(cls, token: dict) -> User | None:
        """Create a user record from the provided JWT token.

        Use the values found in the vaild JWT for the realm
        to populate the User audit data
        """
        if token:
            conf = current_app.config
            user = User(
                username=token.get(conf.get("JWT_OIDC_USERNAME"), None),
                firstname=token.get(conf.get("JWT_OIDC_FIRSTNAME"), None),
                lastname=token.get(conf.get("JWT_OIDC_LASTNAME"), None),
                iss=token["iss"],
                sub=token["sub"],
                idp_userid=token["idp_userid"],
                login_source=token["loginSource"],
            )
            current_app.logger.debug(f"Creating user JWT:{token}; User:{user}")
            user.save()
            return user
        return None

    @classmethod
    def get_or_create_user_by_jwt(cls, jwt_oidc_token) -> User:
        """Return a valid user for audit tracking purposes."""
        # GET existing or CREATE new user based on the JWT info
        try:
            user = User.find_by_jwt_token(jwt_oidc_token)
            current_app.logger.debug(f"finding user: {jwt_oidc_token}")
            if not user:
                current_app.logger.debug(f"didnt find user, create new user:{jwt_oidc_token}")
                user = User.create_from_jwt_token(jwt_oidc_token)

            return user
        except Exception as err:
            current_app.logger.error(err.with_traceback(None))
            raise Exception(  # pylint: disable=broad-exception-raised
                "unable_to_get_or_create_user",
                '{"code": "unable_to_get_or_create_user",'
                '"description": "Unable to get or create user from the JWT"}',
            ) from err

    @classmethod
    def find_by_username(cls, username) -> User | None:
        """Return the oldest User record for the provided username."""
        return cls.query.filter_by(username=username).order_by(User.creation_date.desc()).first()

    @classmethod
    def find_by_sub(cls, sub) -> User | None:
        """Return a User based on the unique sub field."""
        return cls.query.filter_by(sub=sub).one_or_none()

    def save(self):
        """Store the User into the local cache."""
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Store the User into the local cache."""
        db.session.commit()

    def delete(self):
        """Cannot delete User records."""
        return self
        # need to intercept the ORM and stop Users from being deleted

    @classmethod
    @user_context
    def find_user_in_context(cls, **kwargs) -> User:
        """Find the user in context."""
        usr_context: UserContext = kwargs["user_context"]
        if usr_context and usr_context.token_info:
            return User.find_by_jwt_token(usr_context.token_info)
        return None
