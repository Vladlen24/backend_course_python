

from repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.shemas.users import User



class UsersRepository(BaseRepository):
    
    model = UsersOrm
    schema = User