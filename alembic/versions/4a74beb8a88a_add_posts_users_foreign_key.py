"""add posts_users foreign key

Revision ID: 4a74beb8a88a
Revises: 65ed7ce04c9c
Create Date: 2023-12-01 16:53:03.553744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4a74beb8a88a"
down_revision: Union[str, None] = "65ed7ce04c9c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer, nullable=False))
    op.create_foreign_key(
        "fk_posts_users",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("fk_posts_users", table_name="posts")
    op.drop_column("posts", "owner_id")
