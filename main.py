import json
from typing import Sequence
import httpx
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from models import Note
import models
import schemas
import crud_notes
import auth
import crud_users
from database import get_db

app = FastAPI(title="Test notes")

YANDEX_SPELLER_URL = "https://speller.yandex.net/services/spellservice.json/checkText"


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud_users.get_user(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password,
                                            user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/notes/", response_model=list[schemas.Note])
async def read_notes(db: AsyncSession = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)) -> \
Sequence[Note]:
    notes = await crud_notes.get_notes(db, user_id=current_user.id)
    return notes


async def check_spelling(text: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(YANDEX_SPELLER_URL, params={"text": text})
        if not response.content:
            return []

        try:
            return response.json()
        except json.JSONDecodeError:
            return []


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
