from aiogram import Router, F
from aiogram.types import Message

from app.keyboards import back_to_menu_keyboard

router = Router()


@router.message(F.text == "⚙️ Настройки")
async def show_settings(message: Message):
    await message.answer(
        "⚙️ Настройки\n\nРаздел в разработке.",
        reply_markup=back_to_menu_keyboard(),
    )
