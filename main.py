from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from models import Note
from . import models, schemas, crud_notes, auth
from .dependencies import get_db
from typing import Sequence

app = FastAPI(
    title="Test notes"
)

@app.get("/", response_model=list[schemas.Note])
async def read_notes(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)) -> \
Sequence[Note]:
    notes = await crud_notes.get_notes(db, user_id=current_user.id)
    return notes







