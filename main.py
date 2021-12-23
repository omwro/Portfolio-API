import uvicorn

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

from sql import crud, models, schemas
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:80",
    "http://localhost:443",
    "http://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/visitor")
async def get_visitor(db: Session = Depends(get_db)):
    return crud.get_visitors(db)


@app.post("/visitor", response_model=schemas.Visitor)
async def set_visitor(visitor: schemas.VisitorCreate, request: Request, db: Session = Depends(get_db)):
    return crud.set_visitor(db, visitor, request.client.host)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
