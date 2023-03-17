from ..db.config import database
from ..db.models.invitations import Invitation


def get_invitation(adventure_id: int, email: str) -> Invitation:
    """Get an invitation by adventure ID and email."""
    return (
        database.query(Invitation)
        .filter_by(adventure_id=adventure_id, email=email)
        .first()
    )


def create_invitation(adventure_id: int, email: str) -> Invitation:
    """Create an invitation."""
    invitation = Invitation(adventure_id=adventure_id, email=email)
    database.add(invitation)
    database.commit()
    database.refresh(invitation)
    return invitation
