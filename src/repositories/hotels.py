from sqlalchemy import select, insert, func

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.database import engine


class HotelsRepository(BaseRepository):
    
    model = HotelsOrm
    
    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset):
        
        query = select(self.model)
        if title:
            query = query.filter(func.lower(self.model.title).contains(title.lower()))
        if location:
            query = query.filter(func.lower(self.model.location).contains(location.lower()))
        query = (
            query    
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        
        return result.scalars().all()
    
    