from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import models


async def get_user(db: AsyncSession, username: str)-> models.User:
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()

