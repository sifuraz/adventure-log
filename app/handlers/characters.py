from fastapi import HTTPException

from ..db.models.adventures import Adventure, AdventureRoleEnum
from ..handlers.adventures import get_adventure_player
from ..models.adventures import get_adventure_by_id
from ..models.characters import create_and_link_character


def create_character(name: str, adventure_id: int, user_id: int) -> dict:
    """Create a character."""
    adventure: Adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    adventure_player = get_adventure_player(adventure, user_id)
    if not adventure_player or adventure_player.role != AdventureRoleEnum.player:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create character in this adventure",
        )

    if adventure_player.character:
        raise HTTPException(
            status_code=403,
            detail="You already have a character in this adventure",
        )

    character = create_and_link_character(name, adventure_id, user_id)
    character_dict = {"name": character.name}
    return character_dict
