"""Auth utility functions."""
import hashlib
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from src.auth.config import JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from src.auth.exceptions import InvalidTokenError, TokenExpiredError


def _preprocess_password(password: str) -> bytes:
    """
    Preprocess password to handle bcrypt's 72-byte limit.
    Always hash with SHA-256 first to get a fixed 32-byte output.
    This ensures all passwords are handled consistently and avoids the 72-byte limit.
    """
    # Encode password to bytes
    password_bytes = password.encode('utf-8')
    
    # Hash with SHA-256 to get a fixed 32-byte output
    # This is always safe for bcrypt and handles passwords of any length
    sha256_hash = hashlib.sha256(password_bytes).digest()
    return sha256_hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    The password is preprocessed with SHA-256 before bcrypt verification.
    """
    # Preprocess the password the same way we did when hashing
    processed_password = _preprocess_password(plain_password)
    
    # Verify the preprocessed password against the stored hash
    # hashed_password is a string, so we need to encode it
    try:
        return bcrypt.checkpw(processed_password, hashed_password.encode('utf-8'))
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using SHA-256 + bcrypt.
    This approach:
    1. Hashes the password with SHA-256 first (produces fixed 32-byte output)
    2. Then hashes that with bcrypt
    This ensures compatibility with bcrypt's 72-byte limit while supporting passwords of any length.
    """
    # Preprocess password with SHA-256 to handle length limit
    processed_password = _preprocess_password(password)
    
    # Generate salt and hash the preprocessed password with bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(processed_password, salt)
    
    # Return as string (bcrypt hash is already a string when decoded)
    return hashed.decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode and verify a JWT access token."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTError:
        raise InvalidTokenError()

