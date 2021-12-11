from typing import List, Optional

from pydantic import BaseModel


class VisitorBase(BaseModel):
    website: str
    ip: str
    country: str
    city: str
    useragent: str


class VisitorCreate(VisitorBase):
    datetime: str
    pass


class Visitor(VisitorBase):
    id: int

    class Config:
        orm_mode = True
