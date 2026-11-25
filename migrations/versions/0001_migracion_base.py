"""Migracion base completa del proyecto IS1."""

import sqlalchemy as sa
from alembic import op

revision = "0001_base"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agente_ia",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "categoria",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "etiqueta",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "usuario",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("rol", sa.String(length=7), nullable=False),
        sa.Column("contrasena", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "pregunta",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("titulo", sa.String(), nullable=False),
        sa.Column("cuerpo", sa.String(), nullable=False),
        sa.Column("fechaPubli", sa.String(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("categoria_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["categoria_id"], ["categoria.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "pregunta_etiqueta",
        sa.Column("pregunta_id", sa.Integer(), nullable=False),
        sa.Column("etiqueta_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["etiqueta_id"], ["etiqueta.id"]),
        sa.ForeignKeyConstraint(["pregunta_id"], ["pregunta.id"]),
        sa.PrimaryKeyConstraint("pregunta_id", "etiqueta_id"),
    )

    op.create_table(
        "respuesta",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cuerpo", sa.String(), nullable=False),
        sa.Column("fechaPubli", sa.String(), nullable=False),
        sa.Column("aceptada", sa.Boolean(), nullable=False),
        sa.Column("pregunta_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["pregunta_id"], ["pregunta.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "voto",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tipo", sa.String(length=8), nullable=False),
        sa.Column("fecha", sa.String(), nullable=False),
        sa.Column("usuario_id", sa.Integer(), nullable=False),
        sa.Column("pregunta_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["pregunta_id"], ["pregunta.id"]),
        sa.ForeignKeyConstraint(["usuario_id"], ["usuario.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("voto")
    op.drop_table("respuesta")
    op.drop_table("pregunta_etiqueta")
    op.drop_table("pregunta")
    op.drop_table("usuario")
    op.drop_table("etiqueta")
    op.drop_table("categoria")
    op.drop_table("agente_ia")
