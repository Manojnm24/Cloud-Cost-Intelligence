from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cost
from app import config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cost.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Cloud Cost Intelligence Backend Running"}

@app.get("/health")
def health():
    return {"status": "healthy"}