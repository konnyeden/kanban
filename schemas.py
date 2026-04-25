from pydantic import BaseModel
from typing import Optional


class BoardCreate(BaseModel):
    name: str


class BoardUpdate(BaseModel):
    name: str


class BoardOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ColumnCreate(BaseModel):
    name: str
    position: int


class ColumnUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[int] = None


class ColumnOut(BaseModel):
    id: int
    board_id: int
    name: str
    position: int

    class Config:
        orm_mode = True


class CardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: int
    position: int


class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    column_id: Optional[int] = None
    position: Optional[int] = None


class CardOut(BaseModel):
    id: int
    board_id: int
    column_id: int
    title: str
    description: Optional[str] = None
    position: int

    class Config:
        orm_mode = True
