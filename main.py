import portfolio.visitor as visitor
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/portfolio")
async def get_portfolio():
    return {"message": "Hello Portfolio website"}


@app.get("/visitor", response_model=schemas.Visitor)
async def get_visitor(db: Session = Depends(get_db)):
    return crud.get_visitors(db)


@app.post("/visitor", response_model=schemas.Visitor)
async def set_visitor(visitor: schemas.VisitorCreate, db: Session = Depends(get_db)):
    return crud.set_visitor(db, visitor)
