from pydantic import BaseModel, EmailStr
from datetime import datetime
# from pydantic.types import conint

# User Schema
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Post Schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True


# Vote Schema
class Vote(BaseModel):
    post_id: int
    like: bool
    # dir : conint(ge-0,le=1) # less than or equal to


# Authentication Schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str | None = None