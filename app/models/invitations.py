from ..db.config import database
from ..db.models.invitations import Invitation, InvitationStatusEnum


def get_invitations(
    adventure_id: int, email: str, status: InvitationStatusEnum
) -> list[Invitation]:
    """Get an invitation by adventure ID and email."""
    return (
        database.query(Invitation)
        .filter_by(adventure_id=adventure_id, email=email, status=status)
        .all()
    )


def get_pending_invitations_for_email(email: str) -> list[Invitation]:
    """Get all pending invitations by email."""
    return (
        database.query(Invitation)
        .filter_by(email=email, status=InvitationStatusEnum.pending)
        .all()
    )


def create_invitation(adventure_id: int, email: str) -> Invitation:
    """Create an invitation."""
    invitation = Invitation(adventure_id=adventure_id, email=email)
    database.add(invitation)
    database.commit()
    database.refresh(invitation)
    return invitation


def set_invitation_status(
    invitation: Invitation, status: InvitationStatusEnum
) -> Invitation:
    """Set an invitation status."""
    invitation.status = status
    database.commit()
    database.refresh(invitation)
    return invitation
