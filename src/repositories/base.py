from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


from src.database import engine


class BaseRepository:
    
    
    def __init__(self, session):
        self.session = session
    
    async def get_all(self):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
    
    async def add(self, data: BaseModel):
        statement = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(statement)
        # statement = insert(self.model).returning(self.model)
        # result = await self.session.scalars(statement, data.model_dump())

        return result.scalars().one()
        
        
    async def edit(self, id, data):
        statement = (
            update(self.model)
            .where(self.model.id == id)
            .values(data.model_dump())
        )
        await self.session.execute(statement)
    
    
    async def delete(self, id):
        statement = (
            delete(self.model)
            .where(self.model.id == id)
        )
        await self.session.execute(statement)