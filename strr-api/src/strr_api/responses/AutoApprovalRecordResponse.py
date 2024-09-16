"""
AutoApprovalRecord response object.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from strr_api import models
from strr_api.responses import AutoApproval


class AutoApprovalRecord(BaseModel):
    """AutoApprovalRecord response object."""

    id: int
    applicationId: Optional[int]
    applicationNumber: str
    record: AutoApproval
    creationDate: datetime

    @classmethod
    def from_db(cls, source: models.AutoApprovalRecord):
        """Return an AutoApprovalRecord object from a database model."""
        return cls(
            id=source.id,
            applicationId=source.application_id,
            applicationNumber=source.application_number,
            record=AutoApproval(**source.record),
            creationDate=source.creation_date,
        )
