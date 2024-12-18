from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from ..database import session_opener
from .schemas import UserAuthSchema
from ..auth.service import (check_user_password_is_correct,create_access_token,pwd_context,authenticate_user_token)
from ..auth.models import User
import logging
from sentry_sdk import capture_exception
router = APIRouter(
    prefix='/users',
    tags=["Users", "v1"],
)

@router.post(path='/login')
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(session_opener)
):
    """login"""
    logging.debug(f"Login initialised: {form_data.username}")
    user = check_user_password_is_correct(database, form_data.username, form_data.password)
    if not user:
        logging.debug(f"Failed to login: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    try:
        access_token = create_access_token(
        data={"sub": str(user.username)}, expires_delta=timedelta(minutes=30)
    )
    except Exception as e:
        capture_exception(e)
        return HTTPException(status_code=400, detail="Something went wrong while processing the request")
    logging.debug(f"Logged in: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


@router.post(path='/register')
def create_user(user: UserAuthSchema, database: Session = Depends(session_opener)):
    """create user"""
    logging.debug(f"Creating user: {user.username}")
    hashed_password = pwd_context.hash(user.password)
    database_user = User(username=user.username, hashed_password=hashed_password)
    database.add(database_user)

    try:
        database.commit()
    except Exception as e:
        logging.warning(f"Failed to create user: {user.username}, {e}, skipping.")
        capture_exception(e)
        database.rollback()
        return HTTPException(status_code=400, detail="Failed to create user")

    database.refresh(database_user)
    return database_user

@router.get(path='/me')
def read_users_me(user=Depends(authenticate_user_token)):
    logging.debug(f"Accessed /api/v1/users/me: {user.username}")
    return {"username": user.username}