from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from ..db.models.users import User
from ..handlers import adventures
from ..schemas.adventures import AdventureCreate


router = APIRouter()


@router.post("/adventure", status_code=201)
def create_adventure(user: User, adventure: AdventureCreate):
    adventure_id = adventures.create_adventure(adventure.name, adventure.type, user.id)
    return RedirectResponse(url=f"/adventure/{adventure.id}", status_code=303)
