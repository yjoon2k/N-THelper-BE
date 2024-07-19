from fastapi import FastAPI
from app.controller.auth_controller import router as auth_router
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
