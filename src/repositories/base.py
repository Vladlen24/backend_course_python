from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import status


from src.database import engine


class BaseRepository:
    model = None
    schema = None
    
    def __init__(self, session):
        self.session = session
    
    
    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        result = result.scalars().all()
        
        return [self.schema.model_validate(sql_model, from_attributes=True) for sql_model in result]
    
    
    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        result = result.scalars().one_or_none()
        
        if result != None:
            result = self.schema.model_validate(result, from_attributes=True)
            
        return result
    
    
    async def add(self, data: BaseModel):
        statement = insert(self.model).values(data.model_dump()).returning(self.model)
        result = await self.session.execute(statement)
        result = result.scalars().one()
        
        return self.schema.model_validate(result, from_attributes=True)
        
        
    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
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
                .values(**data.model_dump(exclude_unset=exclude_unset))
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