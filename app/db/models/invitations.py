from enum import Enum

from sqlalchemy import Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base
from .mixins import TimestampMixin


class InvitationStatusEnum(str, Enum):
    pending = "pending"
    accepted = "accepted"
    declined = "declined"


class Invitation(Base, TimestampMixin):
    __tablename__ = "invitations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    adventure_id: Mapped[int] = mapped_column(
        ForeignKey("adventures.id"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[InvitationStatusEnum] = mapped_column(
        SQLEnum(InvitationStatusEnum),
        nullable=False,
        default=InvitationStatusEnum.pending,
    )

    adventure: Mapped["Adventure"] = relationship(back_populates="invitations")
