from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from ..db.models.users import User
from ..handlers import notes
from ..models.users import get_current_user
from ..schemas.notes import NoteCreate

router = APIRouter()


@router.post("/note", status_code=201)
def create_note(note_create: NoteCreate, user: User = Depends(get_current_user)):
    """Create a session for an adventure."""
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    notes.add_note(
        note_create.is_secret, note_create.session_id, note_create.text, user.id
    )
    return
