"""Cambios para respuestas y votos."""

import sqlalchemy as sa
from alembic import op

revision = "53c54a4d4499"
down_revision = "0001_base"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("respuesta") as batch_op:
        batch_op.add_column(
            sa.Column("autor_id", sa.Integer(), nullable=False)
        )
        batch_op.add_column(
            sa.Column("autor_tipo", sa.String(length=20), nullable=False)
        )

    with op.batch_alter_table("voto") as batch_op:
        batch_op.add_column(
            sa.Column("respuesta_id", sa.Integer(), nullable=True)
        )
        batch_op.alter_column(
            "pregunta_id",
            existing_type=sa.INTEGER(),
            nullable=True,
        )
        batch_op.create_unique_constraint(
            "uq_voto_usuario_pregunta",
            ["usuario_id", "pregunta_id"],
        )
        batch_op.create_unique_constraint(
            "uq_voto_usuario_respuesta",
            ["usuario_id", "respuesta_id"],
        )
        batch_op.create_foreign_key(
            "fk_voto_respuesta_id_respuesta",
            "respuesta",
            ["respuesta_id"],
            ["id"],
        )
        batch_op.create_check_constraint(
            "ck_voto_un_solo_destino",
            """
            (pregunta_id IS NOT NULL AND respuesta_id IS NULL)
            OR
            (pregunta_id IS NULL AND respuesta_id IS NOT NULL)
            """,
        )


def downgrade():
    with op.batch_alter_table("voto") as batch_op:
        batch_op.drop_constraint(
            "ck_voto_un_solo_destino",
            type_="check",
        )
        batch_op.drop_constraint(
            "fk_voto_respuesta_id_respuesta",
            type_="foreignkey",
        )
        batch_op.drop_constraint(
            "uq_voto_usuario_respuesta",
            type_="unique",
        )
        batch_op.drop_constraint(
            "uq_voto_usuario_pregunta",
            type_="unique",
        )
        batch_op.alter_column(
            "pregunta_id",
            existing_type=sa.INTEGER(),
            nullable=False,
        )
        batch_op.drop_column("respuesta_id")

    with op.batch_alter_table("respuesta") as batch_op:
        batch_op.drop_column("autor_tipo")
        batch_op.drop_column("autor_id")
