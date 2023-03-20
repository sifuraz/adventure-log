from ..db.config import database
from ..db.models.characters import Character
from .adventures import get_adventure_player


def create_and_link_character(name: str, adventure_id: int, user_id: int) -> Character:
    """Create a character."""
    character = Character(name=name)
    database.add(character)
    database.commit()
    database.refresh(character)

    adventure_player = get_adventure_player(adventure_id, user_id)
    adventure_player.character = character
    database.commit()

    return character
