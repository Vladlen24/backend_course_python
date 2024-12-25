from fastapi import FastAPI, Query, Body

app = FastAPI()

hotels = [
    {"id": 1, "title": "Sochi", "name": "Hotel_Sochi"},
    {"id": 2, "title": "Dubai", "name": "Hotel_Dubai"},
]


@app.get("/hotels")
def get_hotels(
    id: int | None = Query(None, description="ID number"),
    title: str | None = Query(None, description="Hotel title"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
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


@app.put("/hotels/{hotel_id}")
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


@app.patch("/hotels/{hotel_id}")
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