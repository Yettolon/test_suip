from src.app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(settings.database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def setup_database() -> None:
    from src.app.db.models import Base

    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # если нужно
        await conn.run_sync(Base.metadata.create_all)
