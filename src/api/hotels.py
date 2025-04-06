from typing import List
from fastapi import APIRouter, Query, Body
from sqlalchemy import insert, select

from src.models.hotels import HotelsOrm
from src.shemas.hotels import Hotel, Error
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine

router = APIRouter(prefix="/hotels", tags=["Отели"])



@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="ID number"),
    title: str | None = Query(None, description="Hotel title"),
) -> List[Hotel] | Error:
    
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if id:
            query = query.filter_by(id=id)
        if title:
            query = query.filter_by(title=title)
        query = (
            query    
            .limit(per_page)
            .offset((pagination.page - 1) * per_page)
        )
        result = await session.execute(query)
        hotels = result.scalars().all()
        
    return hotels


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
            "title": "Hotel Paris 3 stars",
            "location": "Efeltower str., 32",
        }
    },
    "2": {
        "summary": "Dubai",
        "value": {
            "title": "Hotel Abudabi 5 stars",
            "location": "Sand str., 1",
        }
    }
})):
    
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    
    return {"status": "OK"}


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