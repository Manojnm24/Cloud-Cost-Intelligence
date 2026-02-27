from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cost
from app import config
from app.database import engine
from app.models.cost_model import Base
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(cost.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Cloud Cost Intelligence Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}