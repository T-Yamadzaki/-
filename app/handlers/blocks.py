from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.exceptions import TelegramBadRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards import (
    main_menu_keyboard,
    block_card_keyboard,
    product_delete_keyboard,
    confirm_delete_block_keyboard,
    blocks_navigation_keyboard,
    back_to_menu_keyboard,
    cancel_keyboard,
    edit_block_actions_keyboard,
    confirm_usage_keyboard,
    duplicate_keyboard,
)
from app.services import BlockService
from app.utils import format_date, days_ago, status_label

router = Router()
BLOCKS_PER_PAGE = 5


class EditBlockState(StatesGroup):
    waiting_photo = State()
    waiting_text = State()


@router.message(F.text == "📦 Блоки")
async def list_blocks(message: Message, session: AsyncSession):
    service = BlockService(session)
    blocks = await service.get_blocks()

    if not blocks:
        await message.answer(
            "📦 Блоки не найдены.\n\n"
            'Нажмите "➕ Создать блок", чтобы создать первый блок.',
            reply_markup=main_menu_keyboard(),
        )
        return

    await send_blocks_page(message, blocks, 0)


async def send_blocks_page(message: Message, blocks: list, page: int):
    start = page * BLOCKS_PER_PAGE
    end = start + BLOCKS_PER_PAGE
    page_blocks = blocks[start:end]
    total_pages = (len(blocks) + BLOCKS_PER_PAGE - 1) // BLOCKS_PER_PAGE

    for block in page_blocks:
        product_count = len(block.products)
        text = (
            f"📦 Блок №{block.id}\n"
            f"Товаров: {product_count}/6\n"
            f"Создан: {format_date(block.created_at)}\n"
            f"Последняя группа: {format_date(block.group_last_used)}\n"
            f"Последняя суперцена: {format_date(block.superprice_last_used)}\n"
            f"Редактирован: {format_date(block.last_edited)}\n"
            f"Статус: {status_label(block.status)}"
        )
        await message.answer(text, reply_markup=block_card_keyboard(block.id))

    if total_pages > 1:
        nav_keyboard = blocks_navigation_keyboard(page, total_pages)
        await message.answer(
            f"Страница {page + 1} из {total_pages}",
            reply_markup=nav_keyboard,
        )

    if page == 0 and total_pages <= 1:
        await message.answer(
            "Выберите действие с блоком:",
            reply_markup=back_to_menu_keyboard(),
        )


@router.callback_query(lambda c: c.data.startswith("blocks_page:"))
async def blocks_page_nav(callback: CallbackQuery, session: AsyncSession):
    page = int(callback.data.split(":")[1])
    service = BlockService(session)
    blocks = await service.get_blocks()

    if callback.message:
        await callback.message.delete()

    await send_blocks_page(
        callback.message,
        blocks,
        page,  # type: ignore[arg-type]
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("view_block:"))
async def view_block(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)
    block = await service.get_block(block_id)

    if not block:
        await callback.answer("Блок не найден", show_alert=True)
        return

    if callback.message:
        await callback.message.delete()

    for product in block.products:
        try:
            await callback.message.answer_photo(
                photo=product.photo_file_id,
                caption=product.text,
                reply_markup=product_delete_keyboard(product.id, block_id),
            )
        except TelegramBadRequest:
            await callback.message.answer(
                f"⚠️ Фото недоступно\n\n{product.text}",
                reply_markup=product_delete_keyboard(product.id, block_id),
            )

    await callback.message.answer(
        f"📦 Блок №{block_id} — {len(block.products)} из 6 товаров",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("group_use:"))
async def use_in_group(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)

    needs_warning = await service.needs_usage_warning(block_id)
    if needs_warning:
        if callback.message:
            await callback.message.delete()
            await callback.message.answer(
                "⚠️ Внимание! Блок использовался после последнего редактирования.\n"
                "Пожалуйста, проверьте актуальность товаров перед размещением.",
                reply_markup=confirm_usage_keyboard(block_id, "group"),
            )
        await callback.answer()
        return

    block = await service.use_in_group(block_id)

    if callback.message:
        await callback.message.delete()

    for product in block.products:
        try:
            await callback.message.answer_photo(
                photo=product.photo_file_id, caption=product.text
            )
        except TelegramBadRequest:
            await callback.message.answer(product.text)

    await callback.message.answer(
        f"✅ Блок №{block_id} размещён в группе.",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("superprice_use:"))
async def use_in_superprice(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)

    needs_warning = await service.needs_usage_warning(block_id)
    if needs_warning:
        if callback.message:
            await callback.message.delete()
            await callback.message.answer(
                "⚠️ Внимание! Блок использовался после последнего редактирования.\n"
                "Пожалуйста, проверьте актуальность товаров перед размещением.",
                reply_markup=confirm_usage_keyboard(block_id, "superprice"),
            )
        await callback.answer()
        return

    block = await service.use_in_superprice(block_id)

    if callback.message:
        await callback.message.delete()

    for product in block.products:
        try:
            await callback.message.answer_photo(
                photo=product.photo_file_id, caption=product.text
            )
        except TelegramBadRequest:
            await callback.message.answer(product.text)

    await callback.message.answer(
        f"✅ Блок №{block_id} размещён в суперцене.",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("confirm_group_use:"))
async def confirm_group_use(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)
    block = await service.use_in_group(block_id)

    if callback.message:
        await callback.message.delete()

    for product in block.products:
        try:
            await callback.message.answer_photo(
                photo=product.photo_file_id, caption=product.text
            )
        except TelegramBadRequest:
            await callback.message.answer(product.text)

    await callback.message.answer(
        f"✅ Блок №{block_id} размещён в группе.",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("confirm_superprice_use:"))
async def confirm_superprice_use(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)
    block = await service.use_in_superprice(block_id)

    if callback.message:
        await callback.message.delete()

    for product in block.products:
        try:
            await callback.message.answer_photo(
                photo=product.photo_file_id, caption=product.text
            )
        except TelegramBadRequest:
            await callback.message.answer(product.text)

    await callback.message.answer(
        f"✅ Блок №{block_id} размещён в суперцене.",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("cancel_use:"))
async def cancel_use(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(
        "❌ Размещение отменено.", reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("edit_block:"))
async def edit_block(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)
    block = await service.get_block(block_id)

    if not block:
        await callback.answer("Блок не найден", show_alert=True)
        return

    await service.update_last_edited(block_id)

    if callback.message:
        await callback.message.delete()

    for product in block.products:
        try:
            await callback.message.answer_photo(
                photo=product.photo_file_id,
                caption=product.text,
                reply_markup=product_delete_keyboard(product.id, block_id),
            )
        except TelegramBadRequest:
            await callback.message.answer(
                f"⚠️ Фото недоступно\n\n{product.text}",
                reply_markup=product_delete_keyboard(product.id, block_id),
            )

    product_count = len(block.products)
    await callback.message.answer(
        f"✏️ Редактирование блока №{block_id}\n"
        f"Товаров: {product_count}/6\n"
        f'Нажмите "❌ Удалить товар" под товаром, чтобы удалить его.',
        reply_markup=edit_block_actions_keyboard(block_id, product_count),
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("add_product_to_block:"))
async def add_product_to_block_start(
    callback: CallbackQuery, state: FSMContext, session: AsyncSession
):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)
    block = await service.get_block(block_id)

    if not block:
        await callback.answer("Блок не найден", show_alert=True)
        return

    if len(block.products) >= 6:
        await callback.answer("Блок уже содержит 6 товаров", show_alert=True)
        return

    await state.update_data(block_id=block_id, product_count=len(block.products))
    await state.set_state(EditBlockState.waiting_photo)

    await callback.message.delete()
    await callback.message.answer(
        f"📸 Отправьте фото товара {len(block.products) + 1} из 6:",
        reply_markup=cancel_keyboard(),
    )
    await callback.answer()


@router.message(F.text == "❌ Отмена", StateFilter(*EditBlockState))
async def cancel_edit_add(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    block_id = data.get("block_id")
    await state.clear()

    if block_id:
        service = BlockService(session)
        block = await service.get_block(block_id)
        if block:
            for product in block.products:
                try:
                    await message.answer_photo(
                        photo=product.photo_file_id,
                        caption=product.text,
                        reply_markup=product_delete_keyboard(product.id, block_id),
                    )
                except TelegramBadRequest:
                    await message.answer(
                        f"⚠️ Фото недоступно\n\n{product.text}",
                        reply_markup=product_delete_keyboard(product.id, block_id),
                    )

            await message.answer(
                f"✏️ Редактирование блока №{block_id}\nТоваров: {len(block.products)}/6",
                reply_markup=edit_block_actions_keyboard(block_id, len(block.products)),
            )
            return

    await message.answer("❌ Действие отменено.", reply_markup=main_menu_keyboard())


@router.message(EditBlockState.waiting_photo, F.photo)
async def handle_edit_photo(message: Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo_file_id=photo_file_id)
    await state.set_state(EditBlockState.waiting_text)
    await message.answer("📝 Отправьте текст товара:", reply_markup=cancel_keyboard())


@router.message(EditBlockState.waiting_photo)
async def handle_invalid_edit_photo(message: Message):
    await message.answer(
        "❌ Пожалуйста, отправьте фотографию.",
        reply_markup=cancel_keyboard(),
    )


@router.message(EditBlockState.waiting_text, F.text)
async def handle_edit_text(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    block_id = data["block_id"]
    photo_file_id = data["photo_file_id"]

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
    await state.clear()
    await service.update_last_edited(block_id)

    block = await service.get_block(block_id)
    if block:
        for product in block.products:
            try:
                await message.answer_photo(
                    photo=product.photo_file_id,
                    caption=product.text,
                    reply_markup=product_delete_keyboard(product.id, block_id),
                )
            except TelegramBadRequest:
                await message.answer(
                    f"⚠️ Фото недоступно\n\n{product.text}",
                    reply_markup=product_delete_keyboard(product.id, block_id),
                )

        await message.answer(
            f"✏️ Редактирование блока №{block_id}\nТоваров: {new_count}/6",
            reply_markup=edit_block_actions_keyboard(block_id, new_count),
        )


@router.message(EditBlockState.waiting_text)
async def handle_invalid_edit_text(message: Message):
    await message.answer(
        "❌ Пожалуйста, отправьте текстовое описание.",
        reply_markup=cancel_keyboard(),
    )


@router.callback_query(F.data.startswith("force_add:"), StateFilter(*EditBlockState))
async def force_add_product_edit(
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

    await state.clear()
    await callback.message.delete()
    await service.update_last_edited(block_id)

    block = await service.get_block(block_id)
    if block:
        for product in block.products:
            try:
                await callback.message.answer_photo(
                    photo=product.photo_file_id,
                    caption=product.text,
                    reply_markup=product_delete_keyboard(product.id, block_id),
                )
            except TelegramBadRequest:
                await callback.message.answer(
                    f"⚠️ Фото недоступно\n\n{product.text}",
                    reply_markup=product_delete_keyboard(product.id, block_id),
                )

        await callback.message.answer(
            f"✏️ Редактирование блока №{block_id}\nТоваров: {new_count}/6",
            reply_markup=edit_block_actions_keyboard(block_id, new_count),
        )

    await callback.answer()


@router.callback_query(F.data.startswith("cancel_add:"), StateFilter(*EditBlockState))
async def cancel_add_product_edit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "❌ Добавление отменено.", reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("delete_product:"))
async def delete_product(callback: CallbackQuery, session: AsyncSession):
    _, product_id, block_id = callback.data.split(":")
    product_id = int(product_id)
    block_id = int(block_id)

    service = BlockService(session)
    await service.remove_product(product_id, block_id)

    await callback.message.delete()
    await callback.message.answer(
        "✅ Товар удалён.", reply_markup=back_to_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("delete_block:"))
async def delete_block_confirm(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])

    await callback.message.edit_reply_markup(
        reply_markup=confirm_delete_block_keyboard(block_id)
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("confirm_delete_block:"))
async def confirm_delete_block(callback: CallbackQuery, session: AsyncSession):
    block_id = int(callback.data.split(":")[1])
    service = BlockService(session)
    await service.delete_block(block_id)

    await callback.message.delete()
    await callback.message.answer("✅ Блок удалён.", reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("cancel_delete_block:"))
async def cancel_delete_block(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("❌ Удаление отменено.")
    await callback.answer()
