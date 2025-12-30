"""Security utilities."""
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_api_key(api_key: str) -> str:
    """Hash API key for storage."""
    return hashlib.sha256(
        (api_key + settings.API_KEY_SALT).encode()
    ).hexdigest()


def generate_api_key() -> str:
    """Generate a random API key."""
    return secrets.token_urlsafe(32)


def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    """Verify API key against hash."""
    return hash_api_key(plain_key) == hashed_key
