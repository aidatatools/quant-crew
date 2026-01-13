from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.item import Item, ItemCreate, ItemUpdate
from app.services.item import ItemService

router = APIRouter()


@router.get("/", response_model=list[Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> list[Item]:
    service = ItemService(db)
    items = await service.get_items(skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=Item)
async def read_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Item:
    service = ItemService(db)
    item = await service.get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=Item, status_code=201)
async def create_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_db),
) -> Item:
    service = ItemService(db)
    return await service.create_item(item_in)


@router.put("/{item_id}", response_model=Item)
async def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: AsyncSession = Depends(get_db),
) -> Item:
    service = ItemService(db)
    item = await service.update_item(item_id, item_in)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    service = ItemService(db)
    success = await service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
