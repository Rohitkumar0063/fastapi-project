import bcrypt
from passlib.context import CryptContext

# Direct bcrypt use karein instead of passlib
def hashing_password(password: str) -> str:
    """Hash password with bcrypt"""
    # Truncate to 72 bytes
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def verify(plain_password: str, hashed_password: str) -> bool:
    """Verify password"""
    plain_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_bytes, hashed_bytes)