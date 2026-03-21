from fastapi import FastAPI
from app.core.database import Base, engine
from app.models import usuario, rol
from app.core.database import Base, engine
from app.models import *

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Backend Vitiligo Detection System is running"}

@app.get("/health")
def health_check():
    return {"status": "OK"}



Base.metadata.create_all(bind=engine)