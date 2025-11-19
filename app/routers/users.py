from typing import List
from fastapi import APIRouter, status, HTTPException
import sqlalchemy as sa
from app import models, schemas, utils
from app.database import SessionDep

router = APIRouter(
    prefix="/users", 
    tags=["Users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, session: SessionDep):
    hashed_password = utils.get_password_hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())

    
    session.add(new_user)
    try:
        session.commit()
    except sa.exc.IntegrityError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="email alredy exist, please try another email")
    session.refresh(new_user)

    return new_user


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserResponse)
def get_user(id: int, session: SessionDep):
    stmt = sa.select(models.User).where(models.User.id == id)
    try:
        user = session.scalars(stmt).one()
    except sa.exc.NoResultFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"user with id {id} not found")

    return user
    

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserResponse])
def get_user(session: SessionDep):
    stmt = sa.select(models.User)
    user = session.scalars(stmt).all()
   
    return user
    