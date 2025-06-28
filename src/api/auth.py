from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, HTTPException

from passlib.context import CryptContext
import jwt

from src.shemas.users import UserAddRequest, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Authentication & authorization"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@router.post("/register")
async def register_user(data: UserAddRequest):
    
    hashed_password = pwd_context.hash(data.password)
    new_data = UserAdd(login=data.login, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_data)
        await session.commit()
    
    return {"status": "OK"}


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= {"exp": expire}
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


@router.post("/login")
async def login_uer(
    data: UserAddRequest,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким e-mail не найден")
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверно введен пароль пользователя")
        access_token = create_access_token({"user_id": user.id})
        return access_token