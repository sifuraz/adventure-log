from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

from ..db.models.adventures import AdventureTypeEnum
from ..db.models.users import User
from ..handlers import adventures
from ..models.users import get_current_user
from ..schemas.adventures import AdventureCreate, AdventureInvite
from ..settings import templates


router = APIRouter()


@router.post("/adventure", status_code=201)
def create_adventure(
    adventure: AdventureCreate, user: User = Depends(get_current_user)
):
    adventure_id = adventures.create_adventure(adventure.name, adventure.type, user.id)
    return RedirectResponse(url=f"/adventure/{adventure_id}", status_code=303)


@router.get("/adventure/new", response_class=HTMLResponse)
def new_adventure(request: Request, error=None, user: User = Depends(get_current_user)):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse(
        "adventure/new.html",
        {"request": request, "error": error, "types": AdventureTypeEnum, "user": user},
    )


@router.get("/adventure/{adventure_id}", response_class=HTMLResponse)
def show_adventure(
    request: Request,
    adventure_id: int,
    error=None,
    user: User = Depends(get_current_user),
):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    adventure = adventures.get_adventure(adventure_id, user.id)

    return templates.TemplateResponse(
        "adventure/show.html",
        {"request": request, "error": error, "adventure": adventure, "user": user},
    )


@router.post("/adventure/invite", status_code=201)
def invite_player(
    adventure_invite: AdventureInvite, user: User = Depends(get_current_user)
):
    """Invite a player to an adventure."""
    invitation = adventures.invite_player(
        adventure_invite.adventure_id, user.id, adventure_invite.email
    )
    response_data = {"email": invitation.email, "status": invitation.status}
    return JSONResponse(content=response_data)
