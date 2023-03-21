from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base
from .mixins import TimestampMixin


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    date = Column(DateTime, index=True, nullable=False)
    summary = Column(String(255), nullable=True)
    adventure_id: Mapped[int] = mapped_column(
        ForeignKey("adventures.id"), primary_key=True
    )

    adventure: Mapped["Adventure"] = relationship(back_populates="sessions")
