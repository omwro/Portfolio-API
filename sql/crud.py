from datetime import datetime
from sqlalchemy.orm import Session

from sql import models, schemas


def get_visitors(db: Session):
    return db.query(models.Visitor).all()


def set_visitor(db: Session, visitor: schemas.VisitorCreate, ip):
    db_visitor = models.Visitor(
        app=visitor.app,
        uri=visitor.uri,
        ip=ip,
        datetime=datetime.now(),
        useragent=visitor.useragent,
    )
    db.add(db_visitor)
    db.commit()
    db.refresh(db_visitor)
    return db_visitor
