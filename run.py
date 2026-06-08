import asyncio
import logging
from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import TelegramObject

from app.config import settings
from app.database import init_db, async_session
from app.handlers import (
    main_menu,
    create_block,
    blocks,
    incomplete,
    statistics,
    search,
    settings as settings_handler,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with async_session() as session:
            data["session"] = session
            return await handler(event, data)


async def main():
    await init_db()
    logger.info("Database initialized")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware.register(DbSessionMiddleware())

    dp.include_router(main_menu.router)
    dp.include_router(create_block.router)
    dp.include_router(blocks.router)
    dp.include_router(incomplete.router)
    dp.include_router(statistics.router)
    dp.include_router(search.router)
    dp.include_router(settings_handler.router)

    logger.info("Starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
