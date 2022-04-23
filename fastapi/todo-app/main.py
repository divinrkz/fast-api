from fastapi import FastAPI, Depends, HTTPException, APIRouter
import models
from routers import auth, todos
from db import SessionLocal, engine
from starlette.staticfiles import  StaticFiles

app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(auth.router)
app.include_router(todos.router)