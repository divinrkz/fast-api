from fastapi import FastAPI
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


app = FastAPI()

BOOKS = []

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Book description", max_length=10, min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            'example': {
                'id': '12222222222222222222',
                'title': 'Python',
                'author': 'Divin',
                'description': 'tet',
                'rating': 1
            }
        }


@app.get("/")
async def read_all_books():
    return BOOKS



@app.post('/')
async def create_book(book: Book):
    BOOKS.append(book)
    return book
