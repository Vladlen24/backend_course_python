
import json
from fastapi import APIRouter, HTTPException, Response, Request
from starlette.requests import Request


from src.shemas.users import UserAddRequest, UserAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication & authorization"])


@router.post("/register")
async def register_user(data: UserAddRequest):
    
    hashed_password = AuthService().hash_password(data.password)
    new_data = UserAdd(login=data.login, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_data)
        await session.commit()
    
    return {"status": "OK"}


@router.post("/login")
async def login_user(
    data: UserAddRequest,
    response: Response,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(login=data.login)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким e-mail не найден")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Неверно введен пароль пользователя")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
    
    
@router.post("/me")
async def only_auth(
    request: Request,
):
    access_token = request.cookies.get("access_token", None)
    
    return access_token


@router.post("/logout")
async def login_user(
    response: Response,
):
    response.set_cookie("access_token", None)
    return {"status": "OK"}