from pydantic import BaseModel, Field
from typing import Optional


class BookBaseSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    year_published: Optional[int] = None
    isbn: Optional[str] = Field(None, min_length=9, max_length=13)
    copies_available: int = Field(1, ge=0)


class BookCreateSchema(BookBaseSchema):
    pass


class BookUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    year_published: Optional[int] = None
    isbn: Optional[str] = Field(None, min_length=9, max_length=13)
    copies_available: Optional[int] = Field(1, ge=0)


class BookSchema(BookBaseSchema):
    id: int

    class Config:
        from_attributes = True
