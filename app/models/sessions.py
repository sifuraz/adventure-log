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
