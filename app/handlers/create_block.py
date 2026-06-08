from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import (
    main_menu_keyboard,
    cancel_keyboard,
    block_type_keyboard,
    last_used_keyboard,
    duplicate_keyboard,
)
from app.services import BlockService
from app.utils import format_date, days_ago

router = Router()


class CreateBlockState(StatesGroup):
    waiting_block_type = State()
    waiting_last_used = State()
    waiting_photo = State()
    waiting_text = State()


DAYS_MAP = {
    "1-3 дня": 2,
    "4-7 дней": 5,
    "7-14 дней": 10,
    "14+ дней": 20,
}
DAYS_OPTIONS = set(DAYS_MAP.keys())


@router.message(F.text == "➕ Создать блок")
async def create_block_start(
    message: Message, state: FSMContext, session: AsyncSession
):
    service = BlockService(session)
    block_id = await service.create_block()

    await state.update_data(block_id=block_id, product_count=0)
    await state.set_state(CreateBlockState.waiting_block_type)

    await message.answer(
        f"📦 Создан новый блок №{block_id}\n\n📌 Этот блок новый или уже публиковался?",
        reply_markup=block_type_keyboard(),
    )


@router.message(
    CreateBlockState.waiting_block_type, F.text.in_({"🆕 Новый", "📅 Уже публиковался"})
)
async def handle_block_type(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    block_id = data["block_id"]
    service = BlockService(session)
    block = await service.get_block(block_id)
    if not block:
        await message.answer("❌ Ошибка: блок не найден.")
        await state.clear()
        return

    if message.text == "🆕 Новый":
        block.status = "new"
        await session.commit()

        await state.set_state(CreateBlockState.waiting_photo)
        await message.answer(
            f"Отправьте фото товара 1 из 6:",
            reply_markup=cancel_keyboard(),
        )
    else:
        await state.set_state(CreateBlockState.waiting_last_used)
        await message.answer(
            "Когда последний раз использовался?",
            reply_markup=last_used_keyboard(),
        )


@router.message(F.text == "❌ Отмена", StateFilter(*CreateBlockState))
async def cancel_creation(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        "❌ Действие отменено.",
        reply_markup=main_menu_keyboard(),
    )


@router.message(CreateBlockState.waiting_block_type)
async def handle_invalid_block_type(message: Message):
    await message.answer(
        "❌ Пожалуйста, выберите тип блока на клавиатуре.",
        reply_markup=block_type_keyboard(),
    )


@router.message(CreateBlockState.waiting_last_used, F.text.in_(DAYS_OPTIONS))
async def handle_last_used(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    block_id = data["block_id"]
    service = BlockService(session)
    block = await service.get_block(block_id)
    if not block:
        await message.answer("❌ Ошибка: блок не найден.")
        await state.clear()
        return

    days = DAYS_MAP[message.text]
    last_used = datetime.utcnow() - timedelta(days=days)

    block.group_last_used = last_used
    block.superprice_last_used = last_used
    await session.commit()

    await state.set_state(CreateBlockState.waiting_photo)
    await message.answer(
        f"Отправьте фото товара 1 из 6:",
        reply_markup=cancel_keyboard(),
    )


@router.message(CreateBlockState.waiting_last_used)
async def handle_invalid_last_used(message: Message):
    await message.answer(
        "❌ Пожалуйста, выберите период на клавиатуре.",
        reply_markup=last_used_keyboard(),
    )


@router.message(CreateBlockState.waiting_photo, F.photo)
async def handle_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo_file_id=photo_file_id)
    await state.set_state(CreateBlockState.waiting_text)

    await message.answer("📝 Отправьте текст товара:", reply_markup=cancel_keyboard())


@router.message(CreateBlockState.waiting_photo)
async def handle_invalid_photo(message: Message):
    await message.answer(
        "❌ Пожалуйста, отправьте фотографию.",
        reply_markup=cancel_keyboard(),
    )


@router.message(CreateBlockState.waiting_text, F.text)
async def handle_text(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    block_id = data["block_id"]
    photo_file_id = data["photo_file_id"]
    product_count = data.get("product_count", 0)

    service = BlockService(session)
    result = await service.add_product(block_id, photo_file_id, message.text)

    if result.get("duplicate"):
        dup = result["product"]
        await state.update_data(pending_photo=photo_file_id, pending_text=message.text)

        await message.answer(
            f"⚠️ Найден возможный дубликат\n\n"
            f"Номер блока: {dup.block.id}\n"
            f"Дата создания: {format_date(dup.block.created_at)}\n"
            f"Последнее использование: "
            f"{days_ago(dup.block.group_last_used or dup.block.superprice_last_used)}"
        )

        await message.answer_photo(
            photo=dup.photo_file_id,
            caption=dup.text,
            reply_markup=duplicate_keyboard(dup.block_id, block_id),
        )
        return

    new_count = result["count"]
    await state.update_data(product_count=new_count)

    if new_count >= 6:
        await state.clear()
        await message.answer(
            f"✅ Товар добавлен.\n\nБлок №{block_id} готов! Все 6 товаров сохранены.",
            reply_markup=main_menu_keyboard(),
        )
    else:
        await state.set_state(CreateBlockState.waiting_photo)
        await message.answer(
            f"✅ Товар добавлен.\n\n"
            f"В блоке: {new_count} из 6 товаров\n\n"
            f"Отправьте следующее фото:",
            reply_markup=cancel_keyboard(),
        )


@router.message(CreateBlockState.waiting_text)
async def handle_invalid_text(message: Message):
    await message.answer(
        "❌ Пожалуйста, отправьте текстовое описание.",
        reply_markup=cancel_keyboard(),
    )


@router.callback_query(F.data.startswith("force_add:"), StateFilter(*CreateBlockState))
async def force_add_product(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    _, current_block_id = callback.data.split(":")
    block_id = int(current_block_id)
    data = await state.get_data()

    if "pending_photo" not in data or "pending_text" not in data:
        await callback.answer("Ошибка: данные не найдены", show_alert=True)
        return

    service = BlockService(session)
    new_count = await service.add_product_force(
        block_id, data["pending_photo"], data["pending_text"]
    )

    await callback.message.delete()
    await state.update_data(product_count=new_count)

    if new_count >= 6:
        await state.clear()
        await callback.message.answer(
            f"✅ Товар добавлен.\n\nБлок №{block_id} готов! Все 6 товаров сохранены.",
            reply_markup=main_menu_keyboard(),
        )
    else:
        await state.set_state(CreateBlockState.waiting_photo)
        await callback.message.answer(
            f"✅ Товар добавлен.\n\n"
            f"В блоке: {new_count} из 6 товаров\n\n"
            f"Отправьте следующее фото:",
            reply_markup=cancel_keyboard(),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("cancel_add:"), StateFilter(*CreateBlockState))
async def cancel_add_product(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product_count = data.get("product_count", 0)

    await callback.message.delete()
    await state.set_state(CreateBlockState.waiting_photo)
    await callback.message.answer(
        f"❌ Добавление отменено.\n\n"
        f"В блоке: {product_count} из 6 товаров\n\n"
        f"Отправьте следующее фото:",
        reply_markup=cancel_keyboard(),
    )
    await callback.answer()
