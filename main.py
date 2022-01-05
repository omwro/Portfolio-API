import os
from dotenv import load_dotenv
import uvicorn
from fastapi import Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sql import crud, models, schemas
from sql.database import SessionLocal, engine
from util import get_domain_from_origin

models.Base.metadata.create_all(bind=engine)

whitelisted_ips = os.getenv("WHITELIST_IP").split(",")
whitelisted_origins = os.getenv("WHITELIST_ORIGIN").split(",")

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
    client_ip = req.client.host
    client_origin = get_domain_from_origin(req.headers.get("origin"))
    if client_origin in whitelisted_origins or client_ip in whitelisted_ips:
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


@app.get("/visitor/{app_name}")
async def get_visitor_by_app(app_name: str, db: Session = Depends(get_db)):
    return crud.get_visitors_by_app(db, app_name)


@app.get("/visitor/{app_name}/stats")
async def get_visitor_anon_stats_by_app(app_name: str, db: Session = Depends(get_db)):
    return crud.get_visitors_anon_stats_by_app(db, app_name)


@app.post("/visitor", response_model=schemas.Visitor)
async def set_visitor(visitor: schemas.VisitorCreate, request: Request, db: Session = Depends(get_db)):
    return crud.set_visitor(db, visitor, request.client.host)


if __name__ == "__main__":
    load_dotenv()
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app, host="127.0.0.1", port=8000, log_config=log_config)
