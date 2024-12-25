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
"""This exports all of the models and schemas used by the application."""
from .account_roles import AccountRoles
from .address import Address
from .application import Application
from .auto_approval_record import AutoApprovalRecord
from .certificate import Certificate
from .db import db  # noqa: I001
from .dss import DSSOrganization
from .events import Events
from .ltsa import LTSARecord
from .platforms import Platform, PlatformBrand, PlatformRegistration, PlatformRepresentative
from .rental import Document, PropertyContact, PropertyListing, PropertyManager, Registration, RentalProperty
from .strata_hotels import StrataHotel, StrataHotelBuilding, StrataHotelRegistration, StrataHotelRepresentative
from .user import Contact, User

__all__ = (
    "db",
    "AccountRoles",
    "Address",
    "Application",
    "User",
    "RentalProperty",
    "Address",
    "PropertyContact",
    "PropertyListing",
    "PropertyManager",
    "Registration",
    "Contact",
    "Document",
    "Events",
    "DSSOrganization",
    "AutoApprovalRecord",
    "LTSARecord",
    "Certificate",
    "Platform",
    "PlatformBrand",
    "PlatformRegistration",
    "PlatformRepresentative",
    "StrataHotel",
    "StrataHotelRegistration",
    "StrataHotelBuilding",
    "StrataHotelRepresentative",
)
