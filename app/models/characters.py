from ..db.config import database
from ..db.models.adventures import AdventurePlayer
from ..db.models.characters import Character


def create_and_link_character(
    name: str, adventure_player: AdventurePlayer
) -> Character:
    """Create a character."""
    character = Character(name=name)
    database.add(character)
    database.commit()
    database.refresh(character)

    adventure_player.character = character
    database.commit()

    return character
