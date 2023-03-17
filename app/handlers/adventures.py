from fastapi import HTTPException

from ..db.models.adventures import (
    Adventure,
    AdventurePlayer,
    AdventureRoleEnum,
    AdventureTypeEnum,
)
from ..db.models.invitations import Invitation, InvitationStatusEnum
from ..models.adventures import (
    add_adventure_player,
    create_adventure_and_dm,
    get_adventure_by_id,
    get_adventures_by_user_id,
)
from ..models.invitations import create_invitation, get_invitation
from ..models.users import get_user_by_email, User


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
    adventure: Adventure = create_adventure_and_dm(name, adventure_type, user_id)
    return adventure.id


def get_adventure_player(adventure, user_id) -> AdventurePlayer | None:
    """Return user if they are a player in an adventure."""
    for adventure_player in adventure.adventure_players:
        if adventure_player.player_id == user_id:
            return adventure_player
    return None


def is_adventure_dm(adventure, user_id) -> bool:
    """Check if a user is the DM of an adventure."""
    if not (adventure_player := get_adventure_player(adventure, user_id)):
        return False
    return adventure_player.role == AdventureRoleEnum.dm


def get_adventure(adventure_id: int, user_id: int) -> dict:
    """Get an adventure."""
    adventure: Adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if not get_adventure_player(adventure, user_id):
        raise HTTPException(
            status_code=403, detail="You are not allowed to view this adventure"
        )

    adventure_details = adventure_details_dict(adventure)
    adventure_details["pending_invitations"] = get_pending_invitations(adventure)
    return adventure_details


def invite_player(adventure_id: int, user_id: int, email: str) -> dict:
    """Invite a player to an adventure."""
    adventure: Adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if not is_adventure_dm(adventure, user_id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to invite players to this adventure",
        )

    invited_user: User | None = get_user_by_email(email)
    if invited_user and get_adventure_player(adventure, invited_user.id):
        raise HTTPException(status_code=403, detail="Player already in adventure")

    invitation: Invitation | None = get_invitation(adventure_id, email)
    if invitation and invitation.status == InvitationStatusEnum.pending:
        raise HTTPException(status_code=403, detail="Player already invited")

    invitation: Invitation = create_invitation(adventure_id, email)
    invitation_dict = {"email": invitation.email, "status": invitation.status}
    return invitation_dict


def get_pending_invitations(adventure: Adventure) -> list[str]:
    """Get pending invitations for an adventure."""
    invitations = []
    for invitation in adventure.invitations:
        if invitation.status == InvitationStatusEnum.pending:
            invitations.append(invitation.email)
    return invitations


def add_player_to_adventure(adventure_id: int, user_id: int) -> None:
    """Add a player to an adventure."""
    adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if get_adventure_player(adventure, user_id):
        raise HTTPException(status_code=403, detail="Player already in adventure")

    add_adventure_player(adventure_id, user_id)
    return None
