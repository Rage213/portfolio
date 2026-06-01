from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

class EventCreate(BaseModel):
    bot_id: int = Field(..., description="ID телеграм-бота", example=551048892)
    user_id: int = Field(..., description="ID пользователя", example=12345678)
    event_type: str = Field(..., description="Тип события (например, command_start, button_click)", example="command_start")
    details: Optional[str] = Field(None, description="Дополнительные детали в формате JSON строки или текста", example="{'command': '/start'}")

class EventResponse(BaseModel):
    status: str = "success"
    message: str = "Event logged successfully"

class BotStatsResponse(BaseModel):
    bot_id: int
    total_events: int
    active_users: int
    event_breakdown: Dict[str, int]
    activity_over_time: Dict[str, int]

class SystemStatsResponse(BaseModel):
    total_events: int
    active_bots: int
    total_users: int
