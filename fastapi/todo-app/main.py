from fastapi import FastAPI, Depends, HTTPException, APIRouter
import models
from routers import auth, todos
from db import SessionLocal, engine
from company import apis, dependencies

app = FastAPI()
router = APIRouter()

models.Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(
    apis.router,
    dependencies=[Depends(dependencies.get_token_header)],
    prefix='/apis',
    tags=['apis']
)
