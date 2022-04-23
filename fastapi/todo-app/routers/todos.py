import sys

sys.path.append('..')

from starlette import status

from starlette.responses import RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Request, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from pydantic import BaseModel, Field
from typing import Optional
import models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from db import SessionLocal, engine
from . import auth

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# app = FastAPI()
router = APIRouter(
    prefix='/todos',
    tags=['todos'],
    responses={404: {'user': 'Todos not found'}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory='templates')


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Todo(BaseModel):
    title: str
    description: Optional[str]
    priority: int = Field(gt=0, lt=6, description='Pririty must be between 1-5')
    complete: bool


@router.get('/test')
async def test(request: Request):
    return templates.TemplateResponse('home.html', {'request': request})


@router.get('/all')
async def read_all_no_auth(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@router.get('/')
async def read_all(user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db.query(models.Todos).all()


@router.get('/by-user', response_class=HTMLResponse)
async def read_all_by_auser(request: Request, db: Session=Depends(get_db)):
    todos = db.query(models.Todos).filter(models.Todos.owner_id == 1).all()
    return templates.TemplateResponse('home.html', {'request': request, 'todos': todos})


@router.get('/add-todo', response_class=HTMLResponse)
async def add_todo(request: Request, db: Session=Depends(get_db)):
    return templates.TemplateResponse('add-todo.html', {'request': request})



@router.get('/user/{user_id}')
async def read_all_by_user(user: dict = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db.query(models.Todos).filter(models.Todos.owner_id == user.get('id')).all()


@router.get('/todo/{todo_id}')
async def read_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model
    raise http_exception()


@router.post('/')
async def create_todo(todo: Todo, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return {
        'status_code': 201,
        'transaction': 'Successful'
    }

@router.post('/add-todo', response_class=HTMLResponse)
async def create_todo(request: Request, title: str = Form(...), description: str = Form(...), priority: int = Form(...), db: Session = Depends(get_db)):
        todo_model = models.Todos()
        todo_model.title = title
        todo_model.description = description
        todo_model.priority = priority
        todo_model.complete = False
        todo_model.owner_id = 1

        db.add(todo_model)
        db.commit()

        return RedirectResponse(url='/todos', status_code=status.HTTP_302_FOUND)


@router.put('/{todo_id}')
async def update_todo(todo_id: int, todo: Todo, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception()
    todo_model.title = todo.title
    todo_model.description = todo.description
    todo_model.priority = todo.priority
    todo_model.complete = todo.complete

    db.add(todo_model)
    db.commit()

    return {
        'status_code': 200,
        'transaction': 'Updated Succesfuly'
    }


@router.delete('/{todo_id}')
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if todo_model is None:
        raise http_exception()

    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    return {
        'status': 200,
        'transaction': 'Succesfull'
    }


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found")
