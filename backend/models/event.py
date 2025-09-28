from pydantic import BaseModel
from typing import Optional, List, Dict
from google.genai.types import Content, Part

class UserInterests(BaseModel):
    categories: List[int]
    preferences: Dict[str, float] = {"max_radius": 10, "min_overlap_hours": 2}

class EventSearchRequest(BaseModel):
    keyword: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    radius: Optional[int] = None
    km: Optional[int] = None
    date_filter: Optional[str] = None
    category_filter: Optional[List[int]] = None
    sort: Optional[Dict[str, int]] = {"start_time": 1}

class Event(BaseModel):
    calendar_entry_id: int
    event_url: Optional[str]
    name: str
    description: str
    start_time: int
    end_time: int
    venue_id: Optional[int]
    venue: Optional[str]
    location: Optional[str]
    street: Optional[str]
    city: Optional[str]
    zip: Optional[str]
    lat: Optional[float]
    lng: Optional[float]

class EventSearchResponse(BaseModel):
    events: List[Event]

class HangoutSuggestion(BaseModel):
    event: Event
    score: float
    free_slot: Optional[Dict[str, str]]

class PlanHangoutRequest(BaseModel):
    user_id: int
    date_filter: str
    lat: Optional[float] = 25.8056
    lng: Optional[float] = -80.1306
    num_suggestions: int = 5

class PlanHangoutResponse(BaseModel):
    suggestions: List[HangoutSuggestion]
    summary: str

class A2AWebhookRequest(BaseModel):
    intent: str
    user_id: str
    parameters: Dict
    content: Optional[Content] = None

class A2AWebhookResponse(BaseModel):
    fulfillment_text: str
    payload: Optional[Dict] = None
    content: Optional[Content] = None