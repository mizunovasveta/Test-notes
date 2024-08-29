from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://default_user:default_password@localhost:5434/default_db"

engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession  # Используем асинхронную сессию
)

async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

Base = declarative_base()