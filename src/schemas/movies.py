from typing import List, Optional
from pydantic import BaseModel
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    """
    Schema for a single movie.
    """

    id: int
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    """
    Schema for a paginated list of movies.
    """
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[int] = None
    next_page: Optional[int] = None
    total_pages: int
    total_items: int

    class Config:
        from_attributes = True
