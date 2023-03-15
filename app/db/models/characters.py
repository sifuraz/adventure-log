from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..config import Base
from .mixins import TimestampMixin


class Character(Base, TimestampMixin):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    # TODO: race, class, subclass, background, alignment, level, etc.

    adventure_players: Mapped[list["AdventurePlayer"]] = relationship(
        back_populates="character"
    )
