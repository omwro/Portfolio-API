from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from sql.database import Base


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    website = Column(String)
    datetime = Column(DateTime)
    ip = Column(String)
    country = Column(String)
    city = Column(String)
    useragent = Column(String)
