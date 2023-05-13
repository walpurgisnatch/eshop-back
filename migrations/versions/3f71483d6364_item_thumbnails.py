"""item thumbnails

Revision ID: 3f71483d6364
Revises: bbe62f5672a9
Create Date: 2023-05-13 20:45:01.834988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f71483d6364'
down_revision = 'bbe62f5672a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.add_column(sa.Column('thumbnail', sa.String(length=127), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('item', schema=None) as batch_op:
        batch_op.drop_column('thumbnail')

    # ### end Alembic commands ###
