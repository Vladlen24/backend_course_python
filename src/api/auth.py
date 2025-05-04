from fastapi import APIRouter, Query, Body

from passlib.context import CryptContext

from src.shemas.users import UserAddRequest, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository

router = APIRouter(prefix="/auth", tags=["Authentication & authorization"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(data: UserAddRequest):
    
    hashed_password = pwd_context.hash(data.password)
    new_data = UserAdd(login=data.login, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_data)
        await session.commit()
    
    return {"status": "OK"}