from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart

from app.keyboards import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "👋 Добро пожаловать в бот управления товарными блоками!\n\n"
        "Используйте кнопки меню для навигации.",
        reply_markup=main_menu_keyboard(),
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("🏠 Главное меню", reply_markup=main_menu_keyboard())
    await callback.answer()
