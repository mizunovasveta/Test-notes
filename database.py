import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(bind=engine,
                                 autoflush=False,
                                 autocommit=False,
                                 class_=AsyncSession)


async def test_db():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT 1")
        print(result.fetchall())


asyncio.run(test_db())
