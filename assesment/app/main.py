from fastapi import FastAPI
from app.api.routes import router
from app.db.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini Event Management System")
app.include_router(router)
