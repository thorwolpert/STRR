# Copyright © 2024 Province of British Columbia
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
"""Base Model."""
import datetime

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from strr_api.models.user import User

from .db import db


class SimpleBaseModel(db.Model):
    """Base class that defines all the common methods."""

    __abstract__ = True

    @staticmethod
    def commit():
        """Commit the session."""
        db.session.commit()

    def flush(self):
        """Save and flush."""
        db.session.add(self)
        db.session.flush()
        return self

    def add_to_session(self):
        """Save and flush."""
        return self.flush()

    def save(self):
        """Save and commit."""
        db.session.add(self)
        db.session.flush()
        db.session.commit()

        return self

    def delete(self):
        """Delete and commit."""
        db.session.delete(self)
        db.session.flush()
        db.session.commit()

    @staticmethod
    def rollback():
        """RollBack."""
        db.session.rollback()

    def reset(self):
        """Reset."""
        if self:
            db.session.delete(self)
            db.session.commit()


class BaseModel(SimpleBaseModel):
    """Base class that defines all the common columns."""

    __abstract__ = True

    @declared_attr
    def created_by_id(cls):  # pylint:disable=no-self-argument, # noqa: N805
        """Return foreign key for created by."""
        return Column(ForeignKey("users.id"), default=cls._get_current_user)

    @declared_attr
    def modified_by_id(cls):  # pylint:disable=no-self-argument, # noqa: N805
        """Return foreign key for modified by."""
        return Column(ForeignKey("users.id"), onupdate=cls._get_current_user)

    @declared_attr
    def created_by(cls):  # pylint:disable=no-self-argument, # noqa: N805
        """Return relationship for created by."""
        return relationship("User", foreign_keys=[cls.created_by_id], post_update=True, uselist=False)

    @declared_attr
    def modified_by(cls):  # pylint:disable=no-self-argument, # noqa: N805
        """Return relationship for modified by."""
        return relationship("User", foreign_keys=[cls.modified_by_id], post_update=True, uselist=False)

    created = Column(DateTime, default=datetime.datetime.now)
    modified = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    @staticmethod
    def _get_current_user():
        user = User.find_user_in_context()
        return user.id if user else None
