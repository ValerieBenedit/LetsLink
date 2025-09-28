import httpx
import hashlib
import time
from sqlalchemy.orm import Session
from backend.db import EventCache
from models.event import EventSearchRequest, EventSearchResponse
from services.interests import get_user_interests
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv("MIAMI_API_BASE_URL")

async def search_events(db: Session, params: EventSearchRequest) -> EventSearchResponse:
    query_hash = hashlib.md5(str(params.dict()).encode()).hexdigest()
    cached = db.query(EventCache).filter(EventCache.query == query_hash).first()
    if cached and cached.timestamp > int(time.time()) - 3600:
        return EventSearchResponse(**cached.response)

    query_params = {k: v for k, v in params.dict().items() if v is not None}
    if params.sort:
        query_params["srt"] = str(params.sort).replace("'", '"')
    if params.category_filter:
        query_params["category_filter"] = ",".join(map(str, params.category_filter))

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/rest/a.pi/events/search", params=query_params)
        response.raise_for_status()
        result = EventSearchResponse(**response.json())
        db.add(EventCache(query=query_hash, response=result.dict(), timestamp=int(time.time())))
        db.commit()
        return result

async def search_events_by_interests(db: Session, user_id: int, date_filter: str, lat: float, lng: float, radius: int) -> EventSearchResponse:
    interests = get_user_interests(db, user_id)
    params = EventSearchRequest(
        date_filter=date_filter,
        lat=lat,
        lng=lng,
        radius=radius,
        category_filter=interests.categories
    )
    return await search_events(db, params)