from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app.config import settings
from app.models import Base


engine = create_async_engine(settings.database_url, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with engine.begin() as conn:

        def migrate(sync_conn):
            from sqlalchemy import inspect

            inspector = inspect(sync_conn)
            columns = [c["name"] for c in inspector.get_columns("blocks")]
            if "last_edited" not in columns:
                sync_conn.exec_driver_sql(
                    "ALTER TABLE blocks ADD COLUMN last_edited DATETIME"
                )

        await conn.run_sync(migrate)
