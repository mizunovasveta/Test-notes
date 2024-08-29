from pydantic import BaseModel, Field
from typing import Optional


class NoteBase(BaseModel):
    title: str
    description: Optional[str] = Field(None, max_length=100)


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    notes: list[Note] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
