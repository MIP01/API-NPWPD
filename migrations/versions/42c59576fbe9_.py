"""empty message

Revision ID: 42c59576fbe9
Revises: 026b4547a010
Create Date: 2024-03-18 11:27:11.665623

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '42c59576fbe9'
down_revision = '026b4547a010'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('NIK',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.String(length=16),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('NIK',
               existing_type=sa.String(length=16),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    # ### end Alembic commands ###
