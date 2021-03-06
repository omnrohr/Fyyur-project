"""empty message

Revision ID: 7bbb5fd98a7e
Revises: b57b895639f1
Create Date: 2021-09-19 18:10:08.411668

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7bbb5fd98a7e'
down_revision = 'b57b895639f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'image_link',
               existing_type=sa.VARCHAR(length=500),
               nullable=True)
    # ### end Alembic commands ###
