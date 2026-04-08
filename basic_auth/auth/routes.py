from fastapi import APIRouter, HTTPException
from schemas.user_schema import UserRegister, UserLogin
from auth.utils import hash_password, verify_password, create_token
from data.fake_db import users_db

router = APIRouter()

@router.post("/register")
def register(user: UserRegister):

    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    users_db[user.email] = {
        "email": user.email,
        "password": hash_password(user.password)
    }

    return {"message": "User registered successfully"}


@router.post("/login")
def login(user: UserLogin):

    db_user = users_db.get(user.email)

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }