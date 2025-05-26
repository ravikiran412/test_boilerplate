from fastapi import FastAPI, APIRouter
from routes.chat.chat import router as chat_router
from services.database import db

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat")

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    await db.connect_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await db.close_db()

app.include_router(api_router)
