import os
from dotenv import load_dotenv
import uvicorn
from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from sql.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

whitelisted_ips = [
    "127.0.0.1",
    os.getenv("ADMIN_IP")
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def ip_whitelist_middleware(req: Request, call_next):
    if req.client.host in whitelisted_ips:
        return await call_next(req)
    return Response(status_code=403, content="You are forbidden to access this perfectly programmed API ")


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
    load_dotenv()
    uvicorn.run(app, host="127.0.0.1", port=8000)
