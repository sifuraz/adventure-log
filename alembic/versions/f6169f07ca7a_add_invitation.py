"""add Invitation

Revision ID: f6169f07ca7a
Revises: ffe0fdd10a91
Create Date: 2023-03-17 20:13:43.517516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "f6169f07ca7a"
down_revision = "ffe0fdd10a91"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "invitations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("adventure_id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column(
            "status",
            sa.Enum("pending", "accepted", "declined", name="invitationstatusenum"),
            nullable=False,
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["adventure_id"],
            ["adventures.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_invitations_created_at"), "invitations", ["created_at"], unique=False
    )
    op.create_index(op.f("ix_invitations_id"), "invitations", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_invitations_id"), table_name="invitations")
    op.drop_index(op.f("ix_invitations_created_at"), table_name="invitations")
    op.drop_table("invitations")
    # ### end Alembic commands ###