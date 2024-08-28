from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas
from models import Note
from typing import Sequence


async def get_notes(db: AsyncSession, user_id: int) -> Sequence[Note]:
    result = await db.execute(select(models.Note).filter(models.Note.owner_id == user_id))
    return result.scalars().all()






