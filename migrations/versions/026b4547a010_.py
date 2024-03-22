"""empty message

Revision ID: 026b4547a010
Revises: d137f063ed45
Create Date: 2024-03-18 10:53:37.556241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '026b4547a010'
down_revision = 'd137f063ed45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pelaporan',
    sa.Column('id_pelaporan', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('bulan_pelaporan', sa.Integer(), nullable=False),
    sa.Column('bulan_pembayaran', sa.Integer(), nullable=False),
    sa.Column('tahun', sa.Integer(), nullable=False),
    sa.Column('omst_jual', sa.Integer(), nullable=False),
    sa.Column('id_users', sa.Integer(), nullable=True),
    sa.Column('pajak_omst_jual', sa.Integer(), nullable=False),
    sa.Column('keterlambatan', sa.Integer(), nullable=True),
    sa.Column('total_pajak', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['id_users'], ['users.id_users'], ),
    sa.PrimaryKeyConstraint('id_pelaporan')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pelaporan')
    # ### end Alembic commands ###