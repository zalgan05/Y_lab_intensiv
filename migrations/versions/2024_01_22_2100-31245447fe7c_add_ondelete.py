"""Add ondelete

Revision ID: 31245447fe7c
Revises: 428fac137bf8
Create Date: 2024-01-22 21:00:41.996476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '31245447fe7c'
down_revision: Union[str, None] = '428fac137bf8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('dishes_submenu_id_fkey', 'dishes', type_='foreignkey')
    op.create_foreign_key(None, 'dishes', 'submenus', ['submenu_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('submenus_menu_id_fkey', 'submenus', type_='foreignkey')
    op.create_foreign_key(None, 'submenus', 'menus', ['menu_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'submenus', type_='foreignkey')
    op.create_foreign_key('submenus_menu_id_fkey', 'submenus', 'menus', ['menu_id'], ['id'])
    op.drop_constraint(None, 'dishes', type_='foreignkey')
    op.create_foreign_key('dishes_submenu_id_fkey', 'dishes', 'submenus', ['submenu_id'], ['id'])
    # ### end Alembic commands ###