from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from ..config import settings
import os

def get_private_key():
    with open(settings.jwt_private_key_path, 'r') as f:
        return f.read()

def get_public_key():
    with open(settings.jwt_public_key_path, 'r') as f:
        return f.read()

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_private_key(), algorithm=settings.jwt_algorithm)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, get_private_key(), algorithm=settings.jwt_algorithm)

def verify_token(token: str) -> dict:
    return jwt.decode(token, get_public_key(), algorithms=[settings.jwt_algorithm])