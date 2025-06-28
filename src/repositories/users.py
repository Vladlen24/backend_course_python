from pydantic import EmailStr
from sqlalchemy import select

from repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.shemas.users import User, UserWithHashedPassword



class UsersRepository(BaseRepository):
    
    model = UsersOrm
    schema = User
    
    async def get_user_with_hashed_password(self, login: str):
        query = select(self.model).filter_by(login=login)
        result = await self.session.execute(query)
        model = result.scalars().one()
        return UserWithHashedPassword.model_validate(model)