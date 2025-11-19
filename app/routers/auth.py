from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.database import SessionDep
import sqlalchemy as sa
from app import schemas, models, utils

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials: schemas.UserLogin, session: SessionDep):
    stmt = sa.select(models.User).where(models.User.email == user_credentials.email)
    try:
        user = session.scalars(stmt).one()
    except sa.exc.NoResultFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = "Invalid Credentials")
    
    if not utils.verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentails")
    
    return {"token": "example token"}
