from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import models
import schemas
from models import Note
from typing import Sequence


async def get_notes(db: AsyncSession, user_id: int) -> Sequence[Note]:
    result = await db.execute(
        select(models.Note).filter(models.Note.owner_id == user_id))
    return result.scalars().all()


async def create_note(db: AsyncSession, note: schemas.NoteCreate,
                      user_id: int) -> models.Note:
    db_note = models.Note(**note.model_dump(), owner_id=user_id)
    db.add(db_note)
    await db.commit()
    await db.refresh(db_note)
    return db_note
