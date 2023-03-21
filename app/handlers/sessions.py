from datetime import datetime

from fastapi import HTTPException

from ..db.models.adventures import Adventure
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
    }

    return session_details
