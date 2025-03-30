from typing import List
from fastapi import APIRouter, Query, Body
from src.shemas.hotels import Hotel, Error
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
     {"id": 1, "title": "Sochi", "name": "sochi"},
     {"id": 2, "title": "Дубай", "name": "dubai"},
     {"id": 3, "title": "Мальдивы", "name": "maldivi"},
     {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
     {"id": 5, "title": "Москва", "name": "moscow"},
     {"id": 6, "title": "Казань", "name": "kazan"},
     {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
 ]


@router.get("")
def get_hotels(
    pagination: PaginationDep,
    id: int | None = Query(None, description="ID number"),
    title: str | None = Query(None, description="Hotel title"),
    name: str | None = Query(None, description="Hotel name")
) -> List[Hotel] | Error:
    
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if name and hotel["name"] != name:
            continue
        hotels_.append(hotel)
    
    page = pagination.page
    per_page = pagination.per_page

    N = len(hotels_)
    if N > page * per_page:
        is_page = True
    else:
        is_page = False

    if is_page:
        response = hotels_[(page - 1) * per_page:][:per_page]
    else:
        response = {"Error": f"No page {page}"}

    return response


@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
def create_hotel(
    title: str = Body(embed = True),
    name: str = Body(embed = True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
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