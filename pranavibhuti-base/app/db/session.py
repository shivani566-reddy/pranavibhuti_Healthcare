# app/db/session.py
"""
Database session — import get_db in every route that needs DB access.

Usage in a route:
    from app.db.session import get_db
    from sqlalchemy.ext.asyncio import AsyncSession

    @router.get("/something")
    async def my_route(db: AsyncSession = Depends(get_db)):
        result = await db.execute(select(MyModel))
        ...
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,     # prints SQL when DEBUG=True — helpful for development
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,      # reconnects if DB connection dropped
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncSession:
    """
    FastAPI dependency — yields one DB session per request.
    Auto-commits on success, auto-rolls back on error.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
