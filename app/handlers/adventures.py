from ..db.models.adventures import Adventure, AdventurePlayer, AdventureTypeEnum
from ..models.adventures import create_adventure_and_dm, get_adventures_by_user_id


def get_adventures_details(user_id: int) -> list[dict]:
    """Get all adventures for a user."""
    adventures: list[Adventure] = get_adventures_by_user_id(user_id)
    if not adventures:
        return []

    # TODO: order by last activity
    adventures_details = []
    for adventure in adventures:
        adventure_details = {
            "id": adventure.id,
            "name": adventure.name,
            "type": adventure.type.value,
            "players": get_adventure_players_details(adventure.adventure_players),
            "characters": get_adventure_characters_details(adventure.adventure_players),
        }
        adventures_details.append(adventure_details)
    return adventures_details


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
    adventure = create_adventure_and_dm(name, adventure_type, user_id)
    return adventure.id
