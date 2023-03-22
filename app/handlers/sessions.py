from datetime import datetime

from fastapi import HTTPException

from ..db.models.adventures import Adventure
from ..db.models.sessions import Session
from ..handlers.adventures import get_adventure_player, is_adventure_dm
from ..models.adventures import get_adventure_by_id
from ..models.sessions import add_session, get_session_by_date, get_session_by_id


def create_session(date_str: str, adventure_id: int, user_id: int) -> None:
    """Add a session to an adventure."""
    adventure: Adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if not is_adventure_dm(adventure, user_id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create sessions in this adventure",
        )

    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    session = get_session_by_date(date, adventure_id)
    if session:
        raise HTTPException(
            status_code=400,
            detail="A session already exists for this date in this adventure",
        )

    add_session(date, adventure_id)
    return


def get_session(adventure_id: int, session_id: int, user_id: int) -> dict:
    """Get a session."""
    adventure: Adventure = get_adventure_by_id(adventure_id)
    if not adventure:
        raise HTTPException(status_code=404, detail="Adventure not found")

    if not get_adventure_player(adventure, user_id):
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view sessions in this adventure",
        )

    session = get_session_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session_details = {
        "id": session.id,
        "date": session.date.strftime("%d. %m. %Y"),
        "summary": session.summary,
        "notes": get_session_notes(session, user_id),
    }

    return session_details


def get_session_notes(session: Session, user_id: int) -> list[dict]:
    """Get a list of notes for a session."""
    is_dm = is_adventure_dm(session.adventure, user_id)
    notes = []
    for note in session.notes:
        if can_view_note(note, user_id, is_dm):
            notes.append(
                {
                    "id": note.id,
                    "text": note.text,
                    "is_public": note.is_public,
                    "is_reviewed": note.is_reviewed,
                    "author_id": note.author_id,
                    "author_username": note.author.username,
                }
            )
    return notes


def can_view_note(note, user_id: int, is_dm: bool) -> bool:
    """Check if a user can view a note."""
    return is_dm or note.is_public or note.author_id == user_id
