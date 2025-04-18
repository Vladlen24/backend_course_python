from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import status


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
        
        
    async def edit(self, data: BaseModel, **filter_by) -> None:
        query = (
            select(self.model)
            .where(self.model.id == filter_by['id'])
        )
        objects_to_edit = await self.session.execute(query)
        N_objects = len(objects_to_edit.scalars().all())
        if N_objects == 0:
            result = JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=None)
        
        elif N_objects > 1:
            result = JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=None)
        
        elif N_objects == 1:
            statement = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump())
            )
            await self.session.execute(statement)
            
            result = JSONResponse(status_code=status.HTTP_200_OK, content=None)
            
        return result
    
    
    async def delete(self, **filter_by) -> None:
        query = (
            select(self.model)
            .where(self.model.id == filter_by['id'])
        )
        objects_to_edit = await self.session.execute(query)
        N_objects = len(objects_to_edit.scalars().all())
        if N_objects == 0:
            result = JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=None)
        
        elif N_objects > 1:
            result = JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=None)
        
        elif N_objects == 1:
            delete_statement = delete(self.model).filter_by(**filter_by)
            await self.session.execute(delete_statement)
            
            result = JSONResponse(status_code=status.HTTP_200_OK, content=None)
            
        return result