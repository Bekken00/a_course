from fastapi import Depends
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session
from typing import Annotated

SQLALCHEMY_URL = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="123456",
    host="localhost",
    port="5432",
    database="forum"
)
# SQLALCHEMY_URL = "postgresql+psycopg2://postgres:123456@localhost:5432/forum"


engine = create_engine(SQLALCHEMY_URL)

def get_session():
    with Session(bind=engine, autoflush=False, autocommit=False) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

