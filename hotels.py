from typing import List
from fastapi import APIRouter, Query, Body
from shemas import Hotel, Error

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
    id: int | None = Query(None, description="ID number"),
    title: str | None = Query(None, description="Hotel title"),
    name: str | None = Query(None, description="Hotel name"),
    page: int | None = Query(1, description="Page number"),
    per_page: int | None = Query(3, description="Number of hotels per page")
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
    
    N = len(hotels_)
    is_page = True
    start = (page - 1) * per_page
    if N > page * per_page:
        end = page * per_page
    elif N > (page - 1) * per_page:
        end = N
    else:
        is_page = False

    if is_page:
        response = hotels_[start:end]
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