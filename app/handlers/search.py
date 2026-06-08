from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import (
    main_menu_keyboard,
    search_cancel_keyboard,
    search_result_keyboard,
)
from app.services import BlockService

router = Router()


class SearchState(StatesGroup):
    waiting_query = State()


@router.message(F.text == "🔍 Поиск по артикулу")
async def search_start(message: Message, state: FSMContext):
    await state.set_state(SearchState.waiting_query)
    await message.answer(
        "🔍 Введите артикул или часть артикула для поиска:",
        reply_markup=search_cancel_keyboard(),
    )


@router.message(SearchState.waiting_query, F.text)
async def search_execute(message: Message, state: FSMContext, session: AsyncSession):
    query = message.text.strip()
    if not query:
        await message.answer("❌ Введите артикул для поиска.")
        return

    service = BlockService(session)
    results = await service.search_products(query)

    if not results:
        await message.answer(
            f"🔍 Поиск по «{query}» — ничего не найдено.",
            reply_markup=main_menu_keyboard(),
        )
        await state.clear()
        return

    await message.answer(f"🔍 Поиск по «{query}» — найдено {len(results)} товаров:")

    for product in results:
        text = (
            f"📦 Блок №{product.block.id}\n"
            f"Артикул: {product.article}\n"
            f"Размер: {product.size}\n"
            f"{product.text}"
        )
        try:
            await message.answer_photo(
                photo=product.photo_file_id,
                caption=text,
                reply_markup=search_result_keyboard(product.block_id),
            )
        except TelegramBadRequest:
            await message.answer(
                f"⚠️ Фото недоступно\n\n{text}",
                reply_markup=search_result_keyboard(product.block_id),
            )

    await state.clear()
    await message.answer("Выберите действие:", reply_markup=main_menu_keyboard())


@router.message(SearchState.waiting_query)
async def search_invalid(message: Message):
    await message.answer(
        "❌ Пожалуйста, введите текстовый запрос.",
        reply_markup=search_cancel_keyboard(),
    )
