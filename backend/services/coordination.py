import math
from typing import List
from models.event import Event, HangoutSuggestion, UserInterests
from datetime import datetime

def find_free_slots(user_events: List[dict], miami_events: List[Event], min_duration_hours: float = 2):
    start_date = min([datetime.fromtimestamp(e["start_time"]) for e in user_events + miami_events], default=datetime.now())
    end_date = max([datetime.fromtimestamp(e["end_time"]) for e in user_events + miami_events], default=datetime.now())
    busy_intervals = [(e["start_time"], e["end_time"]) for e in user_events + [e.dict() for e in miami_events]]
    busy_intervals.sort()
    merged = []
    for interval in busy_intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval)
        else:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
    free_slots = []
    current = start_date.timestamp()
    min_duration = min_duration_hours * 3600
    for start_t, end_t in merged:
        if start_t - current >= min_duration:
            free_slots.append({"start": current, "end": start_t})
        current = max(current, end_t)
    if end_date.timestamp() - current >= min_duration:
        free_slots.append({"start": current, "end": end_date.timestamp()})
    return [
        {"start": datetime.fromtimestamp(slot["start"]).isoformat(), "end": datetime.fromtimestamp(slot["end"]).isoformat()}
        for slot in free_slots
    ]

def plan_perfect_hangouts(
    db: Session, user_id: int, miami_events: List[Event], user_events: List[dict], interests: UserInterests, lat: float, lng: float
) -> List[HangoutSuggestion]:
    suggestions = []
    for event in miami_events:
        interest_match = 1.0 if any(cat in interests.categories for cat in [event.venue_id or 0]) else 0.5
        event_start, event_end = event.start_time, event.end_time
        event_duration = event_end - event_start
        free_slot = None
        for slot in find_free_slots(user_events, [event], interests.preferences["min_overlap_hours"]):
            if slot["start"] <= event_start and slot["end"] >= event_end:
                overlap = event_duration
                free_slot = slot
                break
        availability = overlap / event_duration if event_duration > 0 else 0.0
        event_lat, event_lng = event.lat or lat, event.lng or lng
        distance = math.sqrt((event_lat - lat)**2 + (event_lng - lng)**2) * 69
        proximity = max(0, 1 - (distance / interests.preferences["max_radius"]))
        score = (interest_match + availability + proximity) / 3
        suggestions.append(HangoutSuggestion(event=event, score=score, free_slot=free_slot))
    return sorted(suggestions, key=lambda x: x.score, reverse=True)[:interests.preferences.get("num_suggestions", 5)]