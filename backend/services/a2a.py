from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.event import A2AWebhookRequest, A2AWebhookResponse
from services.events import search_events_by_interests
from services.calendar import fetch_user_events
from services.coordination import plan_perfect_hangouts
from services.interests import get_user_interests
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import asyncio

session_service = InMemorySessionService()

async def handle_a2a_webhook(request: A2AWebhookRequest, db: Session) -> A2AWebhookResponse:
    intent = request.intent
    params = request.parameters
    user_id = int(request.user_id)
    session = session_service.get_session(user_id) or session_service.create_session(user_id)

    if intent == "plan_hangout":
        date_filter = params.get("date_filter", "20250927-20251010")
        start_date, end_date = date_filter.split("-")
        interests = get_user_interests(db, user_id)
        user_events = await fetch_user_events(db, user_id, start_date, end_date)
        miami_events = (await search_events_by_interests(
            db, user_id, date_filter, params.get("lat", 25.8056), params.get("lng", -80.1306), interests.preferences["max_radius"]
        )).events
        suggestions = plan_perfect_hangouts(db, user_id, miami_events, user_events, interests, params.get("lat", 25.8056), params.get("lng", -80.1306))
        llm = LiteLlm(model="gemini-1.5-pro")
        prompt = f"Found {len(suggestions)} hangout suggestions for {date_filter}: "
        for s in suggestions[:3]:
            prompt += f"- {s.event.name} (score: {s.score:.2f}) at {s.event.venue or s.event.location}, "
        response = await llm.generate_content_async(prompt.rstrip(", ") or "No suggestions found.")
        content = Content(parts=[Part(text=response.text)])
        session_service.update_session(session, {"last_response": response.text})
        return A2AWebhookResponse(
            fulfillment_text=response.text,
            payload={"suggestions": [s.dict() for s in suggestions]},
            content=content
        )
    return A2AWebhookResponse(fulfillment_text="Unknown intent")