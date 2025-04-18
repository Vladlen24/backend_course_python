from typing import List
from fastapi import APIRouter, Query, Body

from src.shemas.hotels import Hotel, HotelPATCH, Error
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotel title"),
    location: str | None = Query(None, description="Hotel location"),
) -> List[Hotel] | Error:
    
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(location=location,
                                                       title=title,
                                                       limit=per_page,
                                                       offset=(pagination.page - 1) * per_page
                                                       )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        result = await HotelsRepository(session).get_one_or_none(id=hotel_id)
    
    return result
    
    
@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    
    async with async_session_maker() as session:
        status = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    
    return status


@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Paris",
        "value": {
            "title": "Hotel Deluxe 3 stars",
            "location": "Paris, Efeltower str., 32",
        }
    },
    "2": {
        "summary": "Dubai",
        "value": {
            "title": "Hotel Resort 5 stars",
            "location": "Dubai, Sand str., 1",
        }
    }
})):
    
    async with async_session_maker() as session:
        result = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    
    return {"status": "OK", "data": result}


@router.put("/{hotel_id}")
async def edit_full_hotel(
    hotel_id: int,
    hotel_data: Hotel = Body()
):
    async with async_session_maker() as session:
        status = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return status


@router.patch("/{hotel_id}")
async def edit_partially_hotel(
    hotel_id: int,
    hotel_data: HotelPATCH = Body()
):
    async with async_session_maker() as session:
        status = await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()

    return status