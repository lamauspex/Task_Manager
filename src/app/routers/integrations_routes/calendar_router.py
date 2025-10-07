
""" Назначение: Роуты календаря """


from fastapi import APIRouter
from src.app.integrations.calendar import GoogleCalendarIntegration

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/events/")
async def get_calendar_events():
    integration = GoogleCalendarIntegration()
    events = integration.get_upcoming_events()
    return {"events": events}


@router.post("/create-event/")
async def create_calendar_event(event_data: dict):
    integration = GoogleCalendarIntegration()
    new_event_id = integration.create_event(**event_data)
    return {"event_id": new_event_id}
