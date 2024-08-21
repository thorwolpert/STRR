"""
Auto Approval response objects.
"""
from typing import Optional

from pydantic import BaseModel


class AutoApproval(BaseModel):
    """Auto approval response object."""

    renting: Optional[bool] = None
    serviceProvider: Optional[bool] = None
    prExempt: Optional[bool] = None
    addressMatch: Optional[bool] = None
    businessLicenseRequired: Optional[bool] = None
    businessLicenseRequiredNotProvided: Optional[bool] = None
    businessLicenseRequiredProvided: Optional[bool] = None
    businessLicenseNotRequiredNotProvided: Optional[bool] = None
    titleCheck: Optional[bool] = None
