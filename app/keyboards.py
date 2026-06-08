from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="📦 Блоки")
    builder.button(text="➕ Создать блок")
    builder.button(text="🔍 Поиск по артикулу")
    builder.button(text="🔄 Неполные блоки")
    builder.button(text="📊 Статистика")
    builder.button(text="⚙️ Настройки")
    builder.adjust(2, 2, 2)
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Отмена")
    return builder.as_markup(resize_keyboard=True)


def block_type_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="🆕 Новый")
    builder.button(text="📅 Уже публиковался")
    builder.button(text="❌ Отмена")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)


def last_used_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="1-3 дня")
    builder.button(text="4-7 дней")
    builder.button(text="7-14 дней")
    builder.button(text="14+ дней")
    builder.button(text="❌ Отмена")
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)


def search_cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Отмена")
    return builder.as_markup(resize_keyboard=True)


def block_card_keyboard(block_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👁 Просмотр", callback_data=f"view_block:{block_id}")
    builder.button(
        text="📢 Разместить в группе",
        callback_data=f"group_use:{block_id}",
    )
    builder.button(
        text="🔥 Разместить в суперцене",
        callback_data=f"superprice_use:{block_id}",
    )
    builder.button(
        text="✏️ Редактировать",
        callback_data=f"edit_block:{block_id}",
    )
    builder.button(
        text="🗑 Удалить",
        callback_data=f"delete_block:{block_id}",
    )
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def search_result_keyboard(block_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="👁 Открыть блок", callback_data=f"view_block:{block_id}")
    builder.button(
        text="📢 Разместить в группе",
        callback_data=f"group_use:{block_id}",
    )
    builder.button(
        text="🔥 Разместить в суперцене",
        callback_data=f"superprice_use:{block_id}",
    )
    builder.adjust(2, 1)
    return builder.as_markup()


def confirm_delete_block_keyboard(block_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Да, удалить",
        callback_data=f"confirm_delete_block:{block_id}",
    )
    builder.button(
        text="❌ Отмена",
        callback_data=f"cancel_delete_block:{block_id}",
    )
    builder.adjust(2)
    return builder.as_markup()


def duplicate_keyboard(
    duplicate_block_id: int, current_block_id: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Добавить всё равно",
        callback_data=f"force_add:{current_block_id}",
    )
    builder.button(
        text="❌ Отменить",
        callback_data=f"cancel_add:{current_block_id}",
    )
    builder.button(
        text="👁 Открыть существующий блок",
        callback_data=f"view_block:{duplicate_block_id}",
    )
    builder.adjust(2, 1)
    return builder.as_markup()


def product_delete_keyboard(product_id: int, block_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="❌ Удалить товар",
        callback_data=f"delete_product:{product_id}:{block_id}",
    )
    return builder.as_markup()


def back_to_block_keyboard(block_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="◀️ Назад к блоку",
        callback_data=f"view_block:{block_id}",
    )
    return builder.as_markup()


def merge_keyboard(block_ids: list[int]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    ids_str = ",".join(str(bid) for bid in block_ids)
    builder.button(
        text="🔄 Создать объединённый блок",
        callback_data=f"merge:{ids_str}",
    )
    builder.button(text="❌ Отмена", callback_data="cancel_merge")
    builder.adjust(1)
    return builder.as_markup()


def blocks_navigation_keyboard(page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if page > 0:
        builder.button(text="◀️ Назад", callback_data=f"blocks_page:{page - 1}")
    if page < total_pages - 1:
        builder.button(text="Вперёд ▶️", callback_data=f"blocks_page:{page + 1}")
    builder.adjust(2)
    return builder.as_markup()


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ В главное меню", callback_data="back_to_menu")
    return builder.as_markup()


def edit_block_actions_keyboard(
    block_id: int, product_count: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if product_count < 6:
        builder.button(
            text="➕ Добавить товар", callback_data=f"add_product_to_block:{block_id}"
        )
    builder.button(text="◀️ В главное меню", callback_data="back_to_menu")
    builder.adjust(1)
    return builder.as_markup()


def confirm_usage_keyboard(block_id: int, usage_type: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="✅ Всё проверил, разместить",
        callback_data=f"confirm_{usage_type}_use:{block_id}",
    )
    builder.button(
        text="❌ Отмена",
        callback_data=f"cancel_use:{block_id}",
    )
    builder.adjust(1)
    return builder.as_markup()
