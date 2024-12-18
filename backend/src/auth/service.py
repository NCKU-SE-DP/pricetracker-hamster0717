from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Query, Depends, status, FastAPI
from jose import JWTError, jwt
from .models import User
from .config import get_auth_settings
from ..database import session_opener
from sentry_sdk import capture_exception
from jose.exceptions import ExpiredSignatureError, JWTError
from datetime import datetime, timedelta
import logging
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/login")
auth_settings=get_auth_settings()
def verify(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def check_user_password_is_correct(database, name, pwd):
    user = database.query(User).filter(User.username == name).first()
    try:
        if not verify(pwd, user.hashed_password):
            return False
    except Exception as e:
        logging.error(f"Failed to verify password: {e}")
        capture_exception(e)
        return False
    return user


def authenticate_user_token(
    token = Depends(oauth2_scheme),
    database = Depends(session_opener)
):
    try:
        logging.debug(f"Authenticating token: {token[:10]}...")
        payload = jwt.decode(token, auth_settings.ACCESS_TOKEN_SECRET_KEY, algorithms=[auth_settings.ACCESS_TOKEN_ALGORITHM])
    except ExpiredSignatureError as e:
        logging.error(f"Token expired: {e}")
        capture_exception(e)
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError as e:
        logging.error(f"Token invalid: {e}")
        capture_exception(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        logging.error(f"Failed to authenticate token: {e}")
        capture_exception(e)
        raise HTTPException(status_code=401, detail="Failed to authenticate token")
    return database.query(User).filter(User.username == payload.get("sub")).first()


def create_access_token(data, expires_delta=None):
    """create access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    try:
        encoded_json_webtoken = jwt.encode(to_encode, auth_settings.ACCESS_TOKEN_SECRET_KEY, algorithm=auth_settings.ACCESS_TOKEN_ALGORITHM)
    except Exception as e:
        logging.error(f"Error while encoding with jwt: {e}")
        raise e
    
    return encoded_json_webtoken