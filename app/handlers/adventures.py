from fastapi import HTTPException

from ..db.models.adventures import Adventure, AdventurePlayer, AdventureTypeEnum
from ..models.adventures import (
    add_adventure_player,
    create_adventure_and_dm,
    get_adventure_by_id,
    get_adventures_by_user_id,
)


def get_adventures_details(user_id: int) -> list[dict]:
    """Get all adventures for a user."""
    adventures: list[Adventure] = get_adventures_by_user_id(user_id)
    if not adventures:
        return []

    # TODO: order by last activity
    adventures_details = []
    for adventure in adventures:
        adventures_details.append(adventure_details_dict(adventure))
    return adventures_details


def adventure_details_dict(adventure: Adventure) -> dict:
    """Get an adventure details as dict."""
    adventure_details = {
        "id": adventure.id,
        "name": adventure.name,
        "type": adventure.type.value,
        "players": get_adventure_players_details(adventure.adventure_players),
        "characters": get_adventure_characters_details(adventure.adventure_players),
    }
    return adventure_details


def get_adventure_players_details(
    adventure_players: list[AdventurePlayer],
) -> list[dict]:
    """Get player details for a list of adventure players."""
    players = []
    for adventure_player in adventure_players:
        player = {
            "id": adventure_player.player.id,
            "username": adventure_player.player.username,
            "role": adventure_player.role.value,
        }
        if adventure_player.character:
            player["character"] = {
                "id": adventure_player.character.id,
                "name": adventure_player.character.name,
            }
        players.append(player)
    return players


def get_adventure_characters_details(
    adventure_players: list[AdventurePlayer],
) -> list[dict]:
    """Get character details for a list of adventure players."""
    characters = []
    for adventure_player in adventure_players:
        if not adventure_player.character:
            continue

        character = {
            "id": adventure_player.character.id,
            "name": adventure_player.character.name,
            "player": {
                "id": adventure_player.player.id,
                "username": adventure_player.player.username,
            },
        }
        characters.append(character)
    return characters


def create_adventure(name: str, adventure_type: AdventureTypeEnum, user_id: int):
    """Create a new adventure."""
    # TODO already exists
    adventure = create_adventure_and_dm(name, adventure_type, user_id)
    return adventure.id


def is_adventure_player(adventure, user_id):
    """Check if a user is a player in an adventure."""
    adventure_player_ids = [
        adventure_player.player_id for adventure_player in adventure.adventure_players
    ]
    return user_id in adventure_player_ids


def get_adventure(adventure_id: int, user_id: int) -> dict:
    """Get an adventure."""
    adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if not is_adventure_player(adventure, user_id):
        raise HTTPException(
            status_code=403, detail="You are not allowed to view this adventure"
        )

    return adventure_details_dict(adventure)


def add_player_to_adventure(adventure_id: int, user_id: int):
    """Add a player to an adventure."""
    adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if is_adventure_player(adventure, user_id):
        raise HTTPException(status_code=403, detail="Player already in adventure")

    add_adventure_player(adventure_id, user_id)
    return
