from fastapi import FastAPI, Query, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Optional

from config import settings
import database
import models
from middleware import APIKeyMiddleware

app = FastAPI(
    title="Telegram Bot Analytics API",
    description="Высокопроизводительный микросервис для сбора метрик и аналитики активности Telegram-ботов",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Auth Middleware
app.add_middleware(APIKeyMiddleware)

@app.on_event("startup")
async def startup_event():
    await database.init_db()

@app.post("/events", response_model=models.EventResponse, status_code=status.HTTP_201_CREATED)
async def log_bot_event(event: models.EventCreate):
    await database.log_event(
        bot_id=event.bot_id,
        user_id=event.user_id,
        event_type=event.event_type,
        details=event.details
    )
    return models.EventResponse()

@app.get("/stats/{bot_id}", response_model=models.BotStatsResponse)
async def get_bot_stats(
    bot_id: int,
    days: int = Query(7, description="Период статистики в днях", ge=1, le=90)
):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    stats = await database.get_bot_metrics(bot_id, start_date, end_date)
    return stats

@app.get("/stats", response_model=models.SystemStatsResponse)
async def get_system_wide_stats(
    days: int = Query(7, description="Период статистики в днях", ge=1, le=90)
):
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    stats = await database.get_system_stats(start_date, end_date)
    return stats

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "healthy", "service": "analytics-api"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
