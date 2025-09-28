from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from backend.db import get_db, User
from models.event import PlanHangoutRequest, PlanHangoutResponse, A2AWebhookRequest, A2AWebhookResponse
from services.coordination import plan_perfect_hangouts
from services.events import search_events, search_events_by_interests
from services.calendar import fetch_user_events, store_google_token
from services.a2a import handle_a2a_webhook
from google.adk import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard
from google_auth_oauthlib.flow import Flow
import uvicorn
import os
from dotenv import load_dotenv
from setup_db import create_database_and_user, create_tables
from backend.test_data import add_test_user

load_dotenv()
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    create_database_and_user()
    create_tables()
    add_test_user()

@app.get("/auth/google")
async def auth_google():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("GOOGLE_CLIENT_ID"),
                "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("REDIRECT_URI")]
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return RedirectResponse(authorization_url)

@app.get("/auth/callback")
async def auth_callback(code: str, db: Session = Depends(get_db)):
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": os.getenv("471731544847-tha4ddiks2f2mnr6hbhbqfj8436o7a5d.apps.googleusercontent.com"),
                "client_secret": os.getenv("OCSPX-YOhnZ92c9hXtLmQwDN10L3zU57im"),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [os.getenv("REDIRECT_URI")]
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar.readonly']
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials
    token = {
        "access_token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "scope": credentials.scopes,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret
    }
    store_google_token(db, user_id=1, token=token)
    return {"message": "Google Calendar authorized successfully"}

@app.post("/api/events/search", response_model=EventSearchResponse)
async def search_events_endpoint(params: EventSearchRequest, db: Session = Depends(get_db)):
    return await search_events(db, params)

@app.post("/api/plan-hangout", response_model=PlanHangoutResponse)
async def plan_hangout(request: PlanHangoutRequest, db: Session = Depends(get_db)):
    interests = get_user_interests(db, request.user_id)
    start_date, end_date = request.date_filter.split("-")
    user_events = await fetch_user_events(db, request.user_id, start_date, end_date)
    miami_events = (await search_events_by_interests(db, request.user_id, request.date_filter, request.lat, request.lng, interests.preferences["max_radius"])).events
    suggestions = plan_perfect_hangouts(db, request.user_id, miami_events, user_events, interests, request.lat, request.lng)
    summary = f"Planned {len(suggestions)} hangouts based on your interests."
    return PlanHangoutResponse(suggestions=suggestions, summary=summary)

@app.post("/a2a/invoke-plan", response_model=A2AWebhookResponse)
async def a2a_invoke_plan(request: A2AWebhookRequest, db: Session = Depends(get_db)):
    return await handle_a2a_webhook(request, db)

if __name__ == "__main__":
    agent_card = AgentCard(
        name="LetsLink",
        url="http://localhost:8000",
        description="Plans hangouts in Miami Beach",
        version="1.0.0",
        capabilities={"planning": True},
        skills=[{"name": "plan_hangout", "description": "Suggests events based on interests and availability"}],
        defaultInputModes=["application/json"],
        defaultOutputModes=["application/json"],
        supportsAuthenticatedExtendedCard=True
    )
    a2a_app = to_a2a(app, port=int(os.getenv("A2A_PORT", 8001)), agent_card=agent_card)
    uvicorn.run(a2a_app, host="0.0.0.0", port=8001)