"""add_dataset_fk_cascade

Revision ID: 441738a3d636
Revises: 6115bd730686
Create Date: 2020-09-26 17:28:14.040590

"""
# pylint: skip-file
# flake8: noqa
# mypy: ignore-errors

import geoalchemy2
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "441738a3d636"
down_revision = "6115bd730686"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        "fk_features_dataset_id_datasets", "features", schema="mapt", type_="foreignkey"
    )
    op.create_foreign_key(
        op.f("fk_features_dataset_id_datasets"),
        "features",
        "datasets",
        ["dataset_id"],
        ["id"],
        source_schema="mapt",
        referent_schema="mapt",
        onupdate="CASCADE",
        ondelete="CASCADE",
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(
        op.f("fk_features_dataset_id_datasets"),
        "features",
        schema="mapt",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "fk_features_dataset_id_datasets",
        "features",
        "datasets",
        ["dataset_id"],
        ["id"],
        source_schema="mapt",
        referent_schema="mapt",
    )
    # ### end Alembic commands ###
