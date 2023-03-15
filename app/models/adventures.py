from ..db.config import database
from ..db.models.adventures import (
    Adventure,
    AdventurePlayer,
    AdventureRoleEnum,
    AdventureTypeEnum,
)


def create_adventure(
    name: str, adventure_type: AdventureTypeEnum, user_id: int
) -> Adventure:
    """Create a new adventure."""
    adventure = Adventure(name=name, type=adventure_type)
    database.add(adventure)
    database.commit()
    database.refresh(adventure)

    adventure_players = AdventurePlayer(
        adventure_id=adventure.id, player_id=user_id, role=AdventureRoleEnum.dm
    )
    database.add(adventure_players)
    database.commit()

    return adventure


def get_adventure_by_id(adventure_id: int) -> Adventure:
    ...


def get_adventures_by_user_id(user_id: int) -> list[Adventure]:
    """Get all adventures for a user."""
    adventure_players = (
        database.query(AdventurePlayer).filter_by(player_id=user_id).all()
    )
    adventures = [adventure_player.adventure for adventure_player in adventure_players]
    return adventures
