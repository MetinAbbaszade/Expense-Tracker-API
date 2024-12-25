from fastapi import FastAPI
from sqlalchemy import create_engine
from app.api.v1.endpoints.auth import router as auth_router
from sqlmodel import SQLModel

MySQL_Connection = 'mysql+pymysql://root:M3tin190534@localhost/Expense_Tracker'

app = FastAPI()
engine = create_engine(MySQL_Connection, echo=True)

def create_app():
    
    app.include_router(auth_router)

    return app

def create_db_and_tables():
    SQLModel.metadata.create_all(bind=engine)