from itertools import combinations
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Block
from app.repositories import BlockRepository, ProductRepository
from app.utils import parse_product_text


class BlockService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.block_repo = BlockRepository(session)
        self.product_repo = ProductRepository(session)

    async def create_block(self) -> int:
        block = await self.block_repo.create()
        return block.id

    async def add_product(self, block_id: int, photo_file_id: str, text: str) -> dict:
        article, size = parse_product_text(text)

        duplicate = await self.product_repo.find_duplicate(article, size)
        if duplicate:
            return {"duplicate": True, "product": duplicate}

        max_order = await self.product_repo.max_order(block_id)
        order = max_order + 1

        await self.product_repo.add(block_id, photo_file_id, text, article, size, order)
        new_count = await self.product_repo.count_in_block(block_id)

        if new_count >= 6:
            await self.block_repo.update_status(block_id, "готов")

        return {"duplicate": False, "count": new_count}

    async def add_product_force(
        self, block_id: int, photo_file_id: str, text: str
    ) -> int:
        article, size = parse_product_text(text)

        max_order = await self.product_repo.max_order(block_id)
        order = max_order + 1

        await self.product_repo.add(block_id, photo_file_id, text, article, size, order)
        new_count = await self.product_repo.count_in_block(block_id)

        if new_count >= 6:
            await self.block_repo.update_status(block_id, "готов")

        return new_count

    async def remove_product(self, product_id: int, block_id: int):
        await self.product_repo.delete(product_id)
        count = await self.product_repo.count_in_block(block_id)
        if count < 6:
            await self.block_repo.update_status(block_id, "неполный")

    async def get_block(self, block_id: int) -> Optional[Block]:
        return await self.block_repo.get_by_id(block_id)

    async def get_blocks(self, status: Optional[str] = None) -> list[Block]:
        return await self.block_repo.get_all(status)

    async def get_incomplete_blocks(self) -> list[Block]:
        return await self.block_repo.get_incomplete()

    async def delete_block(self, block_id: int):
        await self.block_repo.delete(block_id)

    async def use_in_group(self, block_id: int) -> Optional[Block]:
        await self.block_repo.update_group_use(block_id)
        return await self.block_repo.get_by_id(block_id)

    async def use_in_superprice(self, block_id: int) -> Optional[Block]:
        await self.block_repo.update_superprice_use(block_id)
        return await self.block_repo.get_by_id(block_id)

    async def update_last_edited(self, block_id: int):
        await self.block_repo.update_last_edited(block_id)

    async def needs_usage_warning(self, block_id: int) -> bool:
        return await self.block_repo.needs_usage_warning(block_id)

    async def get_statistics(self) -> dict:
        return await self.block_repo.get_statistics()

    async def search_products(self, query: str) -> list:
        return await self.product_repo.search_by_article(query)

    async def find_merge_candidates(self) -> Optional[list[Block]]:
        blocks = await self.block_repo.get_incomplete()
        if len(blocks) < 2:
            return None

        blocks_with_counts = [(b, len(b.products)) for b in blocks]

        for r in range(2, len(blocks_with_counts) + 1):
            for combo in combinations(blocks_with_counts, r):
                total = sum(c for _, c in combo)
                if total == 6:
                    return [b for b, _ in combo]

        return None

    async def merge_blocks(self, block_ids: list[int]) -> int:
        all_products = []
        for bid in block_ids:
            block = await self.block_repo.get_by_id(bid)
            if block:
                all_products.extend(block.products)

        new_block = await self.block_repo.create()

        for i, product in enumerate(all_products):
            product.block_id = new_block.id
            product.order = i + 1

        await self.session.commit()

        for bid in block_ids:
            await self.block_repo.update_status(bid, "архив")

        product_count = len(all_products)
        if product_count >= 6:
            await self.block_repo.update_status(new_block.id, "готов")
        else:
            await self.block_repo.update_status(new_block.id, "неполный")

        await self.session.refresh(new_block)
        return new_block.id
