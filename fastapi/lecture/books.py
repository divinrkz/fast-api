from fastapi import FastAPI
from enum import Enum

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title one', 'author': "Author 1"},
    'book_2': {'title': 'Title two', 'author': "Author 2"},
    'book_3': {'title': 'Title three', 'author': "Author 3"},
    'book_4': {'title': 'Title four', 'author': "Author 4"},
    'book_5': {'title': 'Title five', 'author': "Author 5"},
}

class DirectionName(str, Enum):
    north = 'North'
    south = 'South'
    east = 'East'
    west = 'West'


@app.get("/")
async def read_all_books():
    return BOOKS

@app.get('/books/{book_id}')
async def read_book(book_id: int):
    return {'book_title': book_title}


@app.get('/directions/{direction_name}')
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {'Direction': direction_name, 'sub': 'up'}
    if direction_name == DirectionName.south:
        return {'Direction': direction_name, 'sub': 'down'}
    if direction_name == DirectionName.west:
        return {'Direction': direction_name, 'sub': 'left'}
    if direction_name == DirectionName.east:
        return {'Direction': direction_name, 'sub': 'right'}


@app.post('/')
async def create_book(book_title, book_author):
    current_book_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x

    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']


@app.put('/{book_name}')
async def upate_book(book_name: str, book_title, book_author):
    book_info = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_info
    return BOOKS[book_name]

@app.delete('/{book_name}')
async def delete_book(book_name: str):
    if BOOKS[book_name]:
        del BOOKS[book_name]
    return 'Delete successfully'

