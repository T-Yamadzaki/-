from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import case, select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import Block, Product


class BlockRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self) -> Block:
        block = Block()
        self.session.add(block)
        await self.session.commit()
        await self.session.refresh(block)
        return block

    async def get_by_id(self, block_id: int) -> Optional[Block]:
        stmt = (
            select(Block)
            .where(Block.id == block_id)
            .options(selectinload(Block.products))
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def get_all(self, status: Optional[str] = None) -> list[Block]:
        stmt = select(Block).options(selectinload(Block.products))
        if status:
            stmt = stmt.where(Block.status == status)
        stmt = stmt.order_by(
            case((Block.status == "new", 0), else_=1),
            Block.group_last_used.asc().nullsfirst(),
            Block.superprice_last_used.asc().nullsfirst(),
            Block.created_at.desc(),
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_incomplete(self) -> list[Block]:
        stmt = (
            select(Block)
            .options(selectinload(Block.products))
            .where(Block.status.in_(("неполный", "new")))
            .order_by(Block.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return [b for b in result.unique().scalars().all() if len(b.products) < 6]

    async def update_status(self, block_id: int, status: str):
        block = await self.get_by_id(block_id)
        if block:
            block.status = status
            await self.session.commit()

    async def update_group_use(self, block_id: int):
        block = await self.get_by_id(block_id)
        if block:
            block.group_last_used = datetime.utcnow()
            block.group_use_count = (block.group_use_count or 0) + 1
            if block.status == "new":
                product_count = len(block.products)
                block.status = "готов" if product_count >= 6 else "неполный"
            await self.session.commit()

    async def update_superprice_use(self, block_id: int):
        block = await self.get_by_id(block_id)
        if block:
            block.superprice_last_used = datetime.utcnow()
            block.superprice_use_count = (block.superprice_use_count or 0) + 1
            if block.status == "new":
                product_count = len(block.products)
                block.status = "готов" if product_count >= 6 else "неполный"
            await self.session.commit()

    async def update_last_edited(self, block_id: int):
        block = await self.get_by_id(block_id)
        if block:
            block.last_edited = datetime.utcnow()
            await self.session.commit()

    async def needs_usage_warning(self, block_id: int) -> bool:
        block = await self.get_by_id(block_id)
        if not block:
            return False
        if block.group_last_used is None and block.superprice_last_used is None:
            return False
        last_used = block.group_last_used
        if block.superprice_last_used and (
            last_used is None or block.superprice_last_used > last_used
        ):
            last_used = block.superprice_last_used
        last_edit = block.last_edited or block.created_at
        return last_used > last_edit

    async def delete(self, block_id: int):
        block = await self.get_by_id(block_id)
        if block:
            await self.session.delete(block)
            await self.session.commit()

    async def get_statistics(self) -> dict:
        total = await self.session.execute(select(func.count(Block.id)))
        new_blocks = await self.session.execute(
            select(func.count(Block.id)).where(Block.status == "new")
        )
        ready = await self.session.execute(
            select(func.count(Block.id)).where(Block.status == "готов")
        )
        incomplete = await self.session.execute(
            select(func.count(Block.id)).where(Block.status == "неполный")
        )
        archived = await self.session.execute(
            select(func.count(Block.id)).where(Block.status == "архив")
        )
        total_products = await self.session.execute(select(func.count(Product.id)))
        group_uses = await self.session.execute(select(func.sum(Block.group_use_count)))
        superprice_uses = await self.session.execute(
            select(func.sum(Block.superprice_use_count))
        )

        return {
            "total_blocks": total.scalar() or 0,
            "new_blocks": new_blocks.scalar() or 0,
            "ready_blocks": ready.scalar() or 0,
            "incomplete_blocks": incomplete.scalar() or 0,
            "archived_blocks": archived.scalar() or 0,
            "total_products": total_products.scalar() or 0,
            "group_uses": group_uses.scalar() or 0,
            "superprice_uses": superprice_uses.scalar() or 0,
        }


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(
        self,
        block_id: int,
        photo_file_id: str,
        text: str,
        article: str,
        size: str,
        order: int,
    ) -> Product:
        product = Product(
            block_id=block_id,
            photo_file_id=photo_file_id,
            text=text,
            article=article,
            size=size,
            order=order,
        )
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_duplicate(self, article: str, size: str) -> Optional[Product]:
        if not article or not size:
            return None
        stmt = (
            select(Product)
            .where(and_(Product.article == article, Product.size == size))
            .options(selectinload(Product.block))
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def search_by_article(self, query: str) -> list[Product]:
        if not query:
            return []
        stmt = (
            select(Product)
            .where(Product.article.like(f"%{query}%"))
            .options(selectinload(Product.block))
            .order_by(Product.article)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def delete(self, product_id: int):
        product = await self.get_by_id(product_id)
        if product:
            await self.session.delete(product)
            await self.session.commit()

    async def count_in_block(self, block_id: int) -> int:
        stmt = select(func.count(Product.id)).where(Product.block_id == block_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def max_order(self, block_id: int) -> int:
        stmt = select(func.max(Product.order)).where(Product.block_id == block_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0
