from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from ..db.models.users import User
from ..handlers import sessions
from ..models.users import get_current_user
from ..schemas.sessions import SessionCreate

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
