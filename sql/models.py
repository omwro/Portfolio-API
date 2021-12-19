from sqlalchemy import Boolean, Column, Integer, String, DateTime

from sql.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    website = Column(String(255))
    uri = Column(String(255))
    datetime = Column(DateTime)
    ip = Column(String(255))
    country = Column(String(255))
    city = Column(String(255))
    useragent = Column(String(1000))
