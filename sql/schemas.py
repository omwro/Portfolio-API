from pydantic import BaseModel


class VisitorBase(BaseModel):
    website: str
    uri: str
    ip: str
    country: str
    city: str
    useragent: str


class VisitorCreate(VisitorBase):
    pass


class Visitor(VisitorBase):
    id: int

    class Config:
        orm_mode = True
