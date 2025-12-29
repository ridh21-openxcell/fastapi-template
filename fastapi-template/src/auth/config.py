"""Auth module configuration."""
from src.config import settings

# JWT settings
JWT_SECRET_KEY = settings.SECRET_KEY
JWT_ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Password settings
PASSWORD_MIN_LENGTH = 12
PASSWORD_HASH_ALGORITHM = "bcrypt"

