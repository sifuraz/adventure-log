from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func


class TimestampMixin:
    created_at = Column(DateTime, index=True, nullable=False, server_default=func.now())
    # TODO updated_at = Column(DateTime, index=True, nullable=False, onupdate=func.now)
