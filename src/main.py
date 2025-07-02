from fastapi import FastAPI
from src.app.api.routers import router as api_router
from src.app.db.database import setup_database

app = FastAPI(title="SUIP Parser")


@app.on_event("startup")
async def startup() -> None:
    await setup_database()


app.include_router(api_router)
