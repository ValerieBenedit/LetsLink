# main.py
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import databases, sqlalchemy
from dateutil import parser
import uuid

# --- Database setup ---
DATABASE_URL = "sqlite:///./test.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# --- User model ---
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("age", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("gender", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("interests", sqlalchemy.String, nullable=True),  # comma-separated
    sqlalchemy.Column("location_lat", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("location_lon", sqlalchemy.Float, nullable=True),
    sqlalchemy.Column("timezone", sqlalchemy.String, default="UTC"),
)

# --- Date/Event model ---
dates = sqlalchemy.Table(
    "dates",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.String, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("start", sqlalchemy.DateTime),
    sqlalchemy.Column("end", sqlalchemy.DateTime),
    sqlalchemy.Column("venue", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("activity_type", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("metadata", sqlalchemy.String, nullable=True)
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI(title="Couple Date Planner Backend")

# --- Pydantic models ---
class UserCreate(BaseModel):
    name: str
    age: Optional[int] = None
    gender: Optional[str] = None
    interests: Optional[str] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    timezone: Optional[str] = "UTC"

class DateCreate(BaseModel):
    user_id: str
    title: str
    start: str
    end: str
    venue: Optional[str] = None
    activity_type: Optional[str] = None
    metadata: Optional[str] = None

# --- Utility functions ---
def iso_to_dt(s: str) -> datetime:
    return parser.isoparse(s) if s else None

def merge_and_sort_intervals(intervals: List[tuple]) -> List[tuple]:
    if not intervals:
        return []
    intervals = sorted(intervals, key=lambda x: x[0])
    merged = [intervals[0]]
    for s,e in intervals[1:]:
        last_s, last_e = merged[-1]
        if s <= last_e:
            merged[-1] = (last_s, max(last_e, e))
        else:
            merged.append((s,e))
    return merged

def invert_busy_to_free(busy: List[tuple], window_start: datetime, window_end: datetime) -> List[tuple]:
    free = []
    cur = window_start
    for s,e in busy:
        if e <= window_start or s >= window_end:
            continue
        s = max(s, window_start)
        e = min(e, window_end)
        if cur < s:
            free.append((cur, s))
        cur = max(cur, e)
    if cur < window_end:
        free.append((cur, window_end))
    return free

def intersect_intervals(a: List[tuple], b: List[tuple]) -> List[tuple]:
    i = j = 0
    out = []
    while i < len(a) and j < len(b):
        s1,e1 = a[i]
        s2,e2 = b[j]
        smax = max(s1,s2)
        emin = min(e1,e2)
        if smax < emin:
            out.append((smax, emin))
        if e1 <= e2:
            i += 1
        else:
            j += 1
    return out

def generate_date_ideas(user_a, user_b, slots):
    avg_age = ((user_a.get("age") or 25) + (user_b.get("age") or 25)) // 2
    shared_interests = set((user_a.get("interests") or "").split(",")) & set((user_b.get("interests") or "").split(","))

    suggestions = []
    for slot in slots:
        ideas = []
        if "outdoors" in shared_interests:
            ideas.append({"name": "Central Park Walk", "category": "Outdoors"})
        if "coffee" in shared_interests or avg_age < 30:
            ideas.append({"name": "Cozy Cafe", "category": "Cafe"})
        if "museum" in shared_interests or avg_age >= 30:
            ideas.append({"name": "City Art Museum", "category": "Cultural"})
        if not ideas:
            ideas = [{"name": "Rooftop Dinner", "category": "Dining"}]

        suggestions.append({
            "slot": {"start": slot["start"], "end": slot["end"]},
            "date_idea": ideas[0]
        })
    return suggestions

# --- DB helpers ---
async def get_user(user_id: str):
    q = users.select().where(users.c.id == user_id)
    row = await database.fetch_one(q)
    if not row:
        raise HTTPException(404, "User not found")
    return dict(row)

async def get_user_dates(user_id: str, window_start: datetime, window_end: datetime):
    query = dates.select().where(
        (dates.c.user_id == user_id)
        & (dates.c.end > window_start)
        & (dates.c.start < window_end)
    ).order_by(dates.c.start)
    rows = await database.fetch_all(query)
    return [(row["start"], row["end"], row["title"], row["id"]) for row in rows]

# --- Startup/Shutdown ---
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# --- API Endpoints ---
@app.post("/users", summary="Create user")
async def create_user(u: UserCreate):
    uid = str(uuid.uuid4())
    query = users.insert().values(
        id=uid,
        name=u.name,
        age=u.age,
        gender=u.gender,
        interests=u.interests,
        location_lat=u.location_lat,
        location_lon=u.location_lon,
        timezone=u.timezone
    )
    await database.execute(query)
    return {"id": uid, "name": u.name}

@app.post("/dates", summary="Add a date/event")
async def add_date(d: DateCreate):
    user = await get_user(d.user_id)
    start_dt = iso_to_dt(d.start)
    end_dt = iso_to_dt(d.end)
    if start_dt >= end_dt:
        raise HTTPException(400, "start must be before end")
    did = str(uuid.uuid4())
    q = dates.insert().values(
        id=did,
        user_id=d.user_id,
        title=d.title,
        start=start_dt,
        end=end_dt,
        venue=d.venue,
        activity_type=d.activity_type,
        metadata=d.metadata
    )
    await database.execute(q)
    return {"id": did}

@app.post("/import/calendar", summary="Stub: import user calendar")
async def import_calendar(user_id: str, source: str = "phone", ical_url: str = None):
    """
    source: "phone" or "ical"
    ical_url: required if source="ical"
    """
    # Stub: integrate with Google Calendar API or parse iCal file
    return {"status": "stub", "note": "Implement calendar import logic"}

@app.post("/suggest-dates", summary="Suggest 3 personalized date ideas for a couple")
async def suggest_dates(user_a: str, user_b: str, min_duration_minutes: int = 60):
    ua = await get_user(user_a)
    ub = await get_user(user_b)

    # Search window: next 2 weeks
    now = datetime.utcnow()
    ws = now
    we = now + timedelta(days=14)

    # Fetch busy events
    a_busy = await get_user_dates(user_a, ws, we)
    b_busy = await get_user_dates(user_b, ws, we)
    a_intervals = merge_and_sort_intervals([(s,e) for s,e,_,_ in a_busy])
    b_intervals = merge_and_sort_intervals([(s,e) for s,e,_,_ in b_busy])

    a_free = invert_busy_to_free(a_intervals, ws, we)
    b_free = invert_busy_to_free(b_intervals, ws, we)
    common_free = intersect_intervals(a_free, b_free)

    # Filter by min duration
    min_dur = timedelta(minutes=min_duration_minutes)
    filtered_slots = []
    for s,e in common_free:
        if e - s >= min_dur:
            filtered_slots.append({"start": s.isoformat(), "end": (s+min_dur).isoformat()})
            if len(filtered_slots) >= 3:
                break

    # Generate date ideas
    suggestions = generate_date_ideas(ua, ub, filtered_slots)

    return {"date_suggestions": suggestions}
