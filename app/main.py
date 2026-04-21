from fastapi import FastAPI
from models import *
from core.database import Base, engine
from routes import users, auth, predict
from routes import historial
from routes import citas




app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(historial.router)
app.include_router(citas.router)

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Backend Vitiligo Detection System is running"}

@app.get("/health")
def health_check():
    return {"status": "OK"}
from core.database import SessionLocal

@app.get("/test-db")
def test_db():
    db = SessionLocal()
    return {"mensaje": "conexion exitosa con la base de datos"}