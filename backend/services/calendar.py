from sqlalchemy.orm import Session
from backend.db import User
import caldav
from datetime import datetime, timedelta

def store_caldav_credentials(db: Session, user_id: int, caldav_url: str, username: str, password: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.google_token = {"caldav_url": caldav_url, "username": username, "password": password}
    else:
        user = User(id=user_id, email=f"user{user_id}@example.com", google_token={"caldav_url": caldav_url, "username": username, "password": password})
        db.add(user)
    db.commit()

def get_caldav_client(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.google_token:
        raise ValueError("No CalDAV credentials found")
    return caldav.DAVClient(
        url=user.google_token["caldav_url"],
        username=user.google_token["username"],
        password=user.google_token["password"]
    )

async def fetch_user_events(db: Session, user_id: int, start_date: str, end_date: str):
    client = get_caldav_client(db, user_id)
    principal = client.principal()
    calendars = principal.calendars()
    if not calendars:
        raise ValueError("No calendars found")
    calendar = calendars[0]
    start = datetime.strptime(start_date, "%Y%m%d")
    end = datetime.strptime(end_date, "%Y%m%d") + timedelta(days=1)
    events = calendar.date_search(start, end)
    return [
        {
            "start_time": int(event.icalendar_component["dtstart"].dt.timestamp()),
            "end_time": int(event.icalendar_component["dtend"].dt.timestamp()),
            "summary": event.icalendar_component.get("summary", "")
        }
        for event in events
    ]