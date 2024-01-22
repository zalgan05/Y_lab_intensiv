import uuid
from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)


class Submenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    # menu_id = Column(Integer, ForeignKey('menus.id'))
    menu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('menus.id', ondelete='CASCADE')
    )


class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    # submenu_id = Column(Integer, ForeignKey('submenus.id'))
    submenu_id = Column(
        UUID(as_uuid=True),
        ForeignKey('submenus.id', ondelete='CASCADE')
    )
