from typing import Union
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import delete, distinct, func, insert, select, update
from database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from menus.models import Menu, Submenu, Dish
from menus.schemas import (
    DishCreate,
    DishUpdate,
    MenuCreate,
    MenuUpdate,
    SubmenuCreate,
    SubmenuUpdate
)


router = APIRouter(
    prefix='/menus',
    tags=['Menu']
)


@router.get('')
async def get_menus(session: AsyncSession = Depends(get_async_session)):

    query = (
        select(Menu)
        .add_columns(
            func.count(distinct(Submenu.id)).label('submenus_count'),
            func.count(distinct(Dish.id)).label('dishes_count')
        )
        .join(Submenu, Submenu.menu_id == Menu.id, isouter=True)
        .join(Dish, Dish.submenu_id == Submenu.id, isouter=True)
        .group_by(Menu.id)
    )
    result = await session.execute(query)
    # menus = result.scalars().all()
    menus = []
    for row in result.all():
        menu_dict = {
            'id': row.Menu.id,
            'title': row.Menu.title,
            'description': row.Menu.description,
            'submenus_count': row.submenus_count,
            'dishes_count': row.dishes_count
        }
        menus.append(menu_dict)

    return menus


@router.get('/{target_menu_id}')
async def get_menu(
    target_menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    query = (
        select(Menu)
        .add_columns(
            func.count(Submenu.id).label('submenus_count'),
            # func.count(Dish.id).label('dishes_count')
        )
        .join(Submenu, Submenu.menu_id == Menu.id, isouter=True)
        # .join(Dish, Dish.submenu_id == Submenu.id, isouter=True)
        .where(Menu.id == target_menu_id)
        .group_by(Menu.id)
    )
    result = await session.execute(query)
    result = await session.execute(query)
    menu_data = result.first()

    if menu_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='menu not found'
        )

    menu = {
        'id': str(menu_data[0].id),
        'title': menu_data[0].title,
        'description': menu_data[0].description,
        'submenus_count': menu_data.submenus_count,
        'dishes_count': menu_data.dishes_count
    }

    return menu


@router.delete('/{target_menu_id}')
async def delete_menu(
    target_menu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = delete(Menu).where(Menu.id == target_menu_id)
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(
        content={'status': 'success'},
        status_code=status.HTTP_200_OK
    )


@router.post('')
async def add_menu(
    new_menu: MenuCreate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = insert(Menu).values(new_menu.model_dump()).returning(Menu)
    result = await session.execute(stmt)
    created_menu = result.scalar()

    await session.commit()

    response_menu = {
        'id': str(created_menu.id),
        'title': created_menu.title,
        'description': created_menu.description,
    }
    return JSONResponse(
        content=response_menu,
        status_code=status.HTTP_201_CREATED
    )


@router.patch('/{target_menu_id}')
async def update_menu(
    target_menu_id: UUID,
    new_menu: MenuUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        update(Menu).where(Menu.id == target_menu_id)
        .values(new_menu.model_dump())
        .returning(Menu)
    )
    result = await session.execute(stmt)
    updated_menu = result.scalar()
    await session.commit()
    response_menu = {
        'id': str(updated_menu.id),
        'title': updated_menu.title,
        'description': updated_menu.description,
    }
    return JSONResponse(content=response_menu, status_code=status.HTTP_200_OK)


@router.get('/{target_menu_id}/submenus')
async def get_submenus(
    target_menu_id: Union[UUID, str],
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Submenu).where(Submenu.menu_id == target_menu_id)
    result = await session.execute(query)
    submenu = []
    for row in result.all():
        submenu_dict = {
            'id': row.Submenu.id,
            'title': row.Submenu.title,
            'description': row.Submenu.description,
        }
        submenu.append(submenu_dict)

    return submenu


@router.get('/{target_menu_id}/submenus/{target_submenu_id}')
async def get_submenu(
    target_menu_id: Union[UUID, str],
    target_submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Submenu).where(
        Submenu.id == target_submenu_id and Submenu.menu_id == target_menu_id
    )
    result = await session.execute(query)
    submenu = result.scalar()

    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='submenu not found'
        )

    return submenu


@router.post('/{target_menu_id}/submenus')
async def add_submenu(
    target_menu_id: Union[UUID, str],
    new_submenu: SubmenuCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_submenu_data = new_submenu.model_dump()
    new_submenu_data['menu_id'] = str(target_menu_id)
    stmt = insert(Submenu).values(new_submenu_data).returning(Submenu)
    result = await session.execute(stmt)
    created_submenu = result.scalar()
    await session.commit()

    response_submenu = {
        'id': str(created_submenu.id),
        'title': created_submenu.title,
        'description': created_submenu.description,
    }

    return JSONResponse(
        content=response_submenu,
        status_code=status.HTTP_201_CREATED
    )


@router.patch('/{target_menu_id}/submenus/{target_submenu_id}')
async def update_submenu(
    target_menu_id: Union[UUID, str],
    target_submenu_id: UUID,
    new_submenu: SubmenuUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        update(Submenu).where(
            Submenu.id == target_submenu_id
            and Submenu.menu_id == target_menu_id
        )
        .values(new_submenu.model_dump())
        .returning(Submenu)
    )
    result = await session.execute(stmt)
    updated_submenu = result.scalar()
    await session.commit()
    response_submenu = {
        'id': str(updated_submenu.id),
        'title': updated_submenu.title,
        'description': updated_submenu.description,
    }
    return JSONResponse(
        content=response_submenu,
        status_code=status.HTTP_200_OK
    )


@router.delete('/{target_menu_id}/submenus/{target_submenu_id}')
async def delete_submenu(
    target_menu_id: Union[UUID, str],
    target_submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = delete(Submenu).where(
        Submenu.id == target_submenu_id and Submenu.menu_id == target_menu_id
    )
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(
        content={'status': 'success'},
        status_code=status.HTTP_200_OK
    )


@router.get('/{target_menu_id}/submenus/{target_submenu_id}/dishes')
async def get_dishes(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Dish).where(
        Dish.submenu_id == target_submenu_id
        and Submenu.menu_id == target_menu_id
    )
    result = await session.execute(query)
    dish = []
    for row in result.all():
        dish_dict = {
            'id': row.Dish.id,
            'title': row.Dish.title,
            'description': row.Dish.description,
            'price': round(row.Dish.price, 2)
        }
        dish.append(dish_dict)

    return dish


@router.get(
    '/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def get_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    query = select(Dish).where(
        Dish.submenu_id == target_submenu_id
        and Submenu.menu_id == target_menu_id
        and Dish.id == target_dish_id
    )
    result = await session.execute(query)
    dish = result.scalar()

    if dish is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='dish not found'
        )

    return dish


@router.post('/{target_menu_id}/submenus/{target_submenu_id}/dishes')
async def add_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    new_submenu: DishCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_dish_data = new_submenu.model_dump()
    new_dish_data['submenu_id'] = str(target_submenu_id)
    stmt = insert(Dish).values(new_dish_data).returning(Dish)
    result = await session.execute(stmt)
    created_dish = result.scalar()
    await session.commit()

    response_dish = {
        'id': str(created_dish.id),
        'title': created_dish.title,
        'description': created_dish.description,
        'price': created_dish.price
    }

    return JSONResponse(
        content=response_dish,
        status_code=status.HTTP_201_CREATED
    )


@router.patch(
    '/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def update_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    new_dish: DishUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    stmt = (
        update(Dish)
        .where(
            Dish.submenu_id == target_submenu_id
            and Submenu.menu_id == target_menu_id
            and Dish.id == target_dish_id
        )
        .values(new_dish.model_dump())
        .returning(Dish)
    )
    result = await session.execute(stmt)
    updated_dish = result.scalar()
    await session.commit()
    response_dish = {
        'id': str(updated_dish.id),
        'title': updated_dish.title,
        'description': updated_dish.description,
    }
    return JSONResponse(
        content=response_dish,
        status_code=status.HTTP_200_OK
    )


@router.delete(
    '/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
async def delete_dish(
    target_menu_id: UUID,
    target_submenu_id: UUID,
    target_dish_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    stmt = delete(Dish).where(
        Dish.submenu_id == target_submenu_id
        and Submenu.menu_id == target_menu_id
        and Dish.id == target_dish_id
    )
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(
        content={'status': 'success'},
        status_code=status.HTTP_200_OK
    )
