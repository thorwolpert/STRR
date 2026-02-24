# Copyright © 2025 Province of British Columbia
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
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..common.enum import BaseEnum, auto
from .base_model import SimpleBaseModel

if TYPE_CHECKING:
    from .application import Application
    from .rental import Registration
    from .user import User


class CustomerInteraction(SimpleBaseModel):
    __tablename__ = "interactions"

    class ChannelType(BaseEnum):
        EMAIL = auto()
        SMS = auto()
        PHONE = auto()
        SYSTEM = auto()

    class InteractionStatus(BaseEnum):
        SENT = auto()
        DELIVERED = auto()
        FAILED = auto()
        OPENED = auto()

    id: Mapped[int] = mapped_column(primary_key=True)
    interaction_uuid: Mapped[str] = mapped_column(String(36), unique=True, index=True)

    # tracking this was successfully sent, and the run that covered it
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), unique=True, index=True)

    # Enum-based fixed fields
    channel: Mapped[ChannelType] = mapped_column(SQLEnum(ChannelType))
    status: Mapped[InteractionStatus] = mapped_column(SQLEnum(InteractionStatus), default=InteractionStatus.SENT)

    body_content: Mapped[Optional[str]] = mapped_column(Text)

    # Callback transaction link for audit
    notify_reference: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    provider_reference: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    meta_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    customer_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    application_id: Mapped[Optional[int]] = mapped_column(ForeignKey("application.id"), nullable=True, index=True)
    registration_id: Mapped[Optional[int]] = mapped_column(ForeignKey("registrations.id"), nullable=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)

    # --- Relationships ---
    # 'User', 'Application', 'Registration' are string references, making them future refs
    customer: Mapped[Optional["User"]] = relationship(foreign_keys=[customer_id])
    application: Mapped[Optional["Application"]] = relationship(foreign_keys=[application_id])
    registration: Mapped[Optional["Registration"]] = relationship(foreign_keys=[registration_id])
    user: Mapped[Optional["User"]] = relationship(foreign_keys=[user_id])

    # Ensure it this is linked to only 1 of the 3.
    __table_args__ = (
        CheckConstraint(
            func.num_nonnulls(customer_id, application_id, registration_id) == 1,
            name="check_exclusive_owner_interaction",
        ),
    )
