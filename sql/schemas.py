from pydantic import BaseModel


class VisitorBase(BaseModel):
    app: str
    uri: str
    useragent: str


class VisitorCreate(VisitorBase):
    pass


class Visitor(VisitorBase):
    id: int

    class Config:
        orm_mode = True
