"""empty message

Revision ID: d2b36215d461
Revises: 42c59576fbe9
Create Date: 2024-03-18 12:15:27.097508

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd2b36215d461'
down_revision = '42c59576fbe9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pelaporan', schema=None) as batch_op:
        batch_op.alter_column('pajak_omst_jual',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pelaporan', schema=None) as batch_op:
        batch_op.alter_column('pajak_omst_jual',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)

    # ### end Alembic commands ###