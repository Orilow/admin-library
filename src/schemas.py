from datetime import datetime
from pydantic import BaseModel, Field, EmailStr
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


class ReaderBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr = Field(...)


class ReaderCreateSchema(ReaderBaseSchema):
    pass


class ReaderUpdateSchema(BaseModel):
    name: Optional[str] = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None


class ReaderSchema(ReaderBaseSchema):
    id: int

    class Config:
        from_attributes = True


class BorrowedBookCreateSchema(BaseModel):
    book_id: int = Field(..., ge=1)
    reader_id: int = Field(..., ge=1)


class BorrowedBookReturnSchema(BaseModel):
    book_id: int = Field(..., ge=1)
    reader_id: int = Field(..., ge=1)


class BorrowedBookSchema(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime]

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
