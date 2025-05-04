from sqlalchemy import select, func

from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from src.shemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    
    model = HotelsOrm
    schema = Hotel
    
    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset) -> list[schema]:
        
        query = select(self.model)
        
        if title:
            query = query.filter(func.lower(self.model.title).contains(title.strip().lower()))
        if location:
            query = query.filter(func.lower(self.model.location).contains(location.strip().lower()))
        query = (
            query    
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        hotels = result.scalars().all()
        
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in hotels]
    
    