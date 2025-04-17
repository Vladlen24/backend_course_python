from typing import List
from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select, func

from src.models.hotels import HotelsOrm
from src.shemas.hotels import Hotel, Error
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.repositories.hotels import HotelsRepository
from src.repositories.base import BaseRepository

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


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


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
def edit_full_hotel(
    hotel_id: int,
    title: str = Body(embed=True),
    name: str = Body(embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name

    return {"status": "OK"}


@router.patch("/{hotel_id}")
def edit_partially_hotel(
    hotel_id: int,
    title: str | None = Body(None, embed=True),
    name: str | None = Body(None, embed=True)
):
    global hotels
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title:
                hotel["title"] = title
            if name: 
                hotel["name"] = name

    return {"status": "OK"}