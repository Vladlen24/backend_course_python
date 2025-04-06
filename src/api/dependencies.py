from typing import Annotated
from fastapi import Query, Depends
from pydantic import BaseModel


class PaginatationParams(BaseModel):
    page: Annotated[int | None, Query(1, ge=1, description="Page number")]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30, description="Number of hotels per page")]

PaginationDep = Annotated[PaginatationParams, Depends()]