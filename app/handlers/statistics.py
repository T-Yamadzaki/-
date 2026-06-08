from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import back_to_menu_keyboard
from app.services import BlockService

router = Router()


@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message, session: AsyncSession):
    service = BlockService(session)
    stats = await service.get_statistics()

    text = (
        f"📊 Статистика\n\n"
        f"Всего блоков: {stats['total_blocks']}\n"
        f"🆕 Новых: {stats['new_blocks']}\n"
        f"✅ Готовых: {stats['ready_blocks']}\n"
        f"🔄 Неполных: {stats['incomplete_blocks']}\n"
        f"📦 Архивных: {stats['archived_blocks']}\n\n"
        f"📦 Всего товаров: {stats['total_products']}\n\n"
        f"📢 Размещений в группе: {stats['group_uses'] or 0}\n"
        f"🔥 Размещений в суперцене: {stats['superprice_uses'] or 0}"
    )

    await message.answer(text, reply_markup=back_to_menu_keyboard())
