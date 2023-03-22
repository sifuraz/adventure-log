from sqlalchemy import Boolean, Column, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base
from .mixins import TimestampMixin


class Note(Base, TimestampMixin):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text = Column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(default=True)
    is_reviewed: Mapped[bool] = mapped_column(default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="notes")
    session: Mapped["Session"] = relationship(back_populates="notes")
