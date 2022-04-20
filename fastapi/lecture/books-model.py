from fastapi import FastAPI, HTTPException, Request, Form, Header
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID

from starlette import status
from starlette.responses import JSONResponse


app = FastAPI()

BOOKS = []

class NegativeNumberException(Exception):
    def __int__(self, books_to_return):
        self.books_to_return = books_to_return


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: Optional[str] = Field(None, title='Description of book', min_length=1, max_length=100)

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_number(request: Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={'message': 'Hey why do you want many books'}
    )

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

@app.post('/books/login')
async def book_login(username: str = Form(...), password: str = Form(...)):
    return {'Username': username, 'passwor': password}

@app.get("/all_books")
async def read_all_books(books_to_return: Optional[int]= None):
    if books_to_return and books_to_return < 0:
        raise raise_item_cannot_be_found_exception(books_to_return)
    return BOOKS



@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book


@app.delete('/books/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0

    for x in BOOKS:
        counter += 1
        if x.id == book_id:
            del BOOKS[counter -1]
            return f'ID: {book_id} delete'

    raise raise_item_cannot_be_found_exception()



def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail='Book not found',
                         headers={'X-Header_Error'})


app.get('book/rating/{book_id}', response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise  raise_item_cannot_be_found_exception()


app.get('/header')
async def read_header(random_header: Optional[str] = Header(None)):
    return {'Random-Header': 'this is a header'}