from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import (
    main_menu_keyboard,
    merge_keyboard,
    block_card_keyboard,
    back_to_menu_keyboard,
)
from app.services import BlockService
from app.utils import format_date, status_label

router = Router()


@router.message(F.text == "🔄 Неполные блоки")
async def list_incomplete(message: Message, session: AsyncSession):
    service = BlockService(session)
    blocks = await service.get_incomplete_blocks()

    if not blocks:
        await message.answer(
            "✅ Нет неполных блоков.", reply_markup=main_menu_keyboard()
        )
        return

    for block in blocks:
        product_count = len(block.products)
        text = (
            f"📦 Блок №{block.id}\n"
            f"Товаров: {product_count}/6\n"
            f"Создан: {format_date(block.created_at)}\n"
            f"Статус: {status_label(block.status)}"
        )
        await message.answer(text, reply_markup=block_card_keyboard(block.id))

    merge_candidates = await service.find_merge_candidates()
    if merge_candidates:
        blocks_info = "\n".join(
            f"Блок №{b.id} — {len(b.products)} товаров" for b in merge_candidates
        )
        total = sum(len(b.products) for b in merge_candidates)

        await message.answer(
            f"🔄 Найдено возможное объединение\n\n"
            f"{blocks_info}\n"
            f"Итого: {total} из 6 товаров",
            reply_markup=merge_keyboard([b.id for b in merge_candidates]),
        )

    await message.answer("Выберите действие:", reply_markup=back_to_menu_keyboard())


@router.callback_query(lambda c: c.data.startswith("merge:"))
async def execute_merge(callback: CallbackQuery, session: AsyncSession):
    block_ids = [int(bid) for bid in callback.data.split(":")[1].split(",")]

    service = BlockService(session)
    new_block_id = await service.merge_blocks(block_ids)

    await callback.message.delete()
    await callback.message.answer(
        f"✅ Создан объединённый блок №{new_block_id}\n"
        f"Старые блоки перемещены в архив.",
        reply_markup=main_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data == "cancel_merge")
async def cancel_merge(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("❌ Объединение отменено.")
    await callback.answer()
