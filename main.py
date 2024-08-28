from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from models import Note
from . import models, schemas, crud_notes, auth
from .dependencies import get_db
from typing import Sequence
import httpx

app = FastAPI(title="Test notes")


@app.get("/notes/", response_model=list[schemas.Note])
async def read_notes(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)) -> \
Sequence[Note]:
    notes = await crud_notes.get_notes(db, user_id=current_user.id)
    return notes


YANDEX_SPELLER_URL = "https://speller.yandex.net/services/spellservice.json"


async def check_spelling(text: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.post(YANDEX_SPELLER_URL, data={"text": text})
        return response.json()


@app.post("/create_note/", response_model=schemas.Note)
async def create_note_route(
    note: schemas.NoteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
) -> schemas.Note:
    if note.title:
        spelling_errors_title: list[dict] = await check_spelling(note.title)
        if spelling_errors_title:
            corrected_title: str = note.title
            for error in spelling_errors_title:
                if error['s']:
                    corrected_title = corrected_title.replace(
                        error['word'], error['s'][0])

            note.title = corrected_title

    if note.description:
        spelling_errors_description: list[dict] = await check_spelling(
            note.description)
        if spelling_errors_description:
            corrected_description: str = note.description
            for error in spelling_errors_description:
                if error['s']:
                    corrected_description = corrected_description.replace(
                        error['word'], error['s'][0])

            note.description = corrected_description

    return await crud_notes.create_note(db=db,
                                        note=note,
                                        user_id=current_user.id)
