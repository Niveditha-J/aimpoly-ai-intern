from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "aimploy_secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_token(data: dict):

    expire = datetime.utcnow() + timedelta(minutes=60)

    data.update({"exp": expire})

    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return token