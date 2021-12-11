from datetime import datetime
from sqlalchemy.orm import Session

from sql import models, schemas


def get_visitors(db: Session):
    return db.query(models.Visitor).all()


def set_visitor(db: Session, visitor: schemas.VisitorCreate):
    db_visitor = models.Visitor(
        website=visitor.website,
        ip=visitor.ip,
        datetime=datetime.now(),
        country=visitor.country,
        city=visitor.city,
        useragent=visitor.useragent,
    )
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor
