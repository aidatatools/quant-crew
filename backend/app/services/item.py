from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_items(self, skip: int = 0, limit: int = 100) -> list[Item]:
        result = await self.db.execute(select(Item).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def get_item(self, item_id: int) -> Item | None:
        result = await self.db.execute(select(Item).where(Item.id == item_id))
        return result.scalar_one_or_none()

    async def create_item(self, item_in: ItemCreate) -> Item:
        item = Item(**item_in.model_dump())
        self.db.add(item)
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def update_item(self, item_id: int, item_in: ItemUpdate) -> Item | None:
        item = await self.get_item(item_id)
        if item is None:
            return None

        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete_item(self, item_id: int) -> bool:
        item = await self.get_item(item_id)
        if item is None:
            return False

        await self.db.delete(item)
        await self.db.commit()
        return True
