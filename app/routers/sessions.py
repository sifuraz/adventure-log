from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse

from ..db.models.users import User
from ..handlers import sessions
from ..models.users import get_current_user
from ..schemas.sessions import SessionCreate
from ..settings import templates

router = APIRouter()


@router.post("/session", status_code=201)
def create_session(
    session_create: SessionCreate, user: User = Depends(get_current_user)
):
    """Create a session for an adventure."""
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    sessions.create_session(session_create.date, session_create.adventure_id, user.id)
    return


@router.get(
    "/adventure/{adventure_id}/session/{session_id}", response_class=HTMLResponse
)
def show_session(
    request: Request,
    adventure_id: int,
    session_id: int,
    error=None,
    user: User = Depends(get_current_user),
):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    session = sessions.get_session(adventure_id, session_id, user.id)

    return templates.TemplateResponse(
        "session/show.html",
        {"request": request, "error": error, "session": session, "user": user},
    )
