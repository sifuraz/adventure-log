from enum import Enum

from sqlalchemy import Enum as SQLEnum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base
from .mixins import TimestampMixin


class AdventureRoleEnum(str, Enum):
    player = "player"
    dm = "dm"


class AdventureTypeEnum(str, Enum):
    campaign = "campaign"
    one_shot = "one_shot"
    two_shot = "two_shot"


class AdventurePlayer(Base, TimestampMixin):
    __tablename__ = "adventure_players"

    adventure_id: Mapped[int] = mapped_column(
        ForeignKey("adventures.id"), primary_key=True
    )
    player_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    role: Mapped[AdventureRoleEnum] = mapped_column(SQLEnum(AdventureRoleEnum))
    character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=True
    )

    adventure: Mapped["Adventure"] = relationship(back_populates="adventure_players")
    player: Mapped["User"] = relationship(back_populates="adventure_players")
    character: Mapped["Character"] = relationship(back_populates="adventure_players")


class Adventure(Base, TimestampMixin):
    __tablename__ = "adventures"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[AdventureTypeEnum] = mapped_column(SQLEnum(AdventureTypeEnum))

    adventure_players: Mapped[list["AdventurePlayer"]] = relationship(
        back_populates="adventure"
    )
