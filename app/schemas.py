from pydantic import BaseModel, EmailStr, Field
from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import Optional, Annotated


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


@dataclass(config=dict(from_attributes=True))
class User(UserBase):
    id: int
    created_at: datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


@dataclass(config=dict(from_attributes=True))
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User


class PostOut(BaseModel):
    Post: Post
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(ge=0, le=1, strict=True)]
