"""add TimestampMixin

Revision ID: 896608ac1173
Revises: e7373722b374
Create Date: 2023-03-11 22:38:00.073829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "896608ac1173"
down_revision = "e7373722b374"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
    )
    op.create_index(op.f("ix_users_created_at"), "users", ["created_at"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_created_at"), table_name="users")
    op.drop_column("users", "created_at")
    # ### end Alembic commands ###