from fastapi import FastAPI, HTTPException, Response, status, Depends
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlalchemy
from sqlalchemy import select, update, delete
from app import models, schemas, utils
from app.database import engine, SessionDep
from app.models import Base
from app.routers import users, posts, auth



DUP = "dbname=forum user=postgres password=123456"


Base.metadata.create_all(engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "hello world!"}