from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse, RedirectResponse

from ..db.models.users import User
from ..handlers import characters
from ..models.users import get_current_user
from ..schemas.characters import CharacterCreate


router = APIRouter()


@router.post("/character", status_code=201)
def create_character(
    character_create: CharacterCreate, user: User = Depends(get_current_user)
):
    """Create a character for an adventure."""
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    character = characters.create_character(
        character_create.name, character_create.adventure_id, user.id
    )
    return JSONResponse(content=character, status_code=201)
