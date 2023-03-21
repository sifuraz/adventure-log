from datetime import datetime

from ..db.config import database
from ..db.models.sessions import Session


def add_session(date: datetime.date, adventure_id: int) -> Session:
    """Create an adventure session."""
    session = Session(date=date, adventure_id=adventure_id)
    database.add(session)
    database.commit()
    database.refresh(session)
    return session


def get_session_by_date(date: datetime.date, adventure_id: int) -> Session:
    """Get a session by date."""
    return (
        database.query(Session).filter_by(date=date, adventure_id=adventure_id).first()
    )


def get_session_by_id(session_id: int) -> Session:
    """Get a session by id."""
    return database.query(Session).get(session_id)
