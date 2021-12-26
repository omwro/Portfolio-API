from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from sql import schemas
from sql.models import Visitor


def get_visitors(db: Session):
    return db.query(Visitor).all()


def get_visitors_by_app(db: Session, app_name: str):
    return db.query(Visitor).filter(Visitor.app == app_name).all()


def get_visitors_anon_stats_by_app(db: Session, app_name: str):
    lastyear_datetime = datetime.now() - timedelta(days=365)
    return len(db.query(Visitor).filter(Visitor.app == app_name, Visitor.datetime >= lastyear_datetime).all())


def set_visitor(db: Session, visitor: schemas.VisitorCreate, ip):
    db_visitor = Visitor(
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
