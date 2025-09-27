# services/interests.py

# Master list of interests
INTERESTS = [
    "Dining Out",
    "Movies",
    "Art & Museums",
    "Music & Concerts",
    "Sports & Fitness",
    "Nature",
    "Travel & Adventure",
    "Gaming",
    "Reading & Books",
    "Photography",
    "Cooking",
    "Dancing"
]

def get_all_interests() -> list:
    """Return the full list of available interests."""
    return INTERESTS

def validate_interests(selected: list) -> list:
    """
    Validate a list of user-selected interests.
    Returns only the valid interests from the master list.
    """
    return [i for i in selected if i in INTERESTS]

def suggest_activities(shared_interests: list) -> list:
    """
    Generate example date ideas based on shared interests.
    """
    suggestions = []
    for interest in shared_interests:
        if interest == "Dining Out":
            suggestions.append({"name": "Romantic Dinner", "category": "Dining"})
        elif interest == "Movies":
            suggestions.append({"name": "Evening Movie Night", "category": "Entertainment"})
        elif interest == "Art & Museums":
            suggestions.append({"name": "Visit Art Museum", "category": "Cultural"})
        elif interest == "Music & Concerts":
            suggestions.append({"name": "Live Concert", "category": "Entertainment"})
        elif interest == "Sports & Fitness":
            suggestions.append({"name": "Couples Yoga Class", "category": "Fitness"})
        elif interest == "Nature":
            suggestions.append({"name": "Nature Hike", "category": "Outdoors"})
        elif interest == "Travel & Adventure":
            suggestions.append({"name": "Weekend Road Trip", "category": "Adventure"})
        elif interest == "Gaming":
            suggestions.append({"name": "Game Night", "category": "Indoor Fun"})
        elif interest == "Reading & Books":
            suggestions.append({"name": "Visit a Bookstore & Cafe", "category": "Leisure"})
        elif interest == "Photography":
            suggestions.append({"name": "Photography Walk", "category": "Outdoors"})
        elif interest == "Cooking":
            suggestions.append({"name": "Cook Together at Home", "category": "Food"})
        elif interest == "Dancing":
            suggestions.append({"name": "Dance Class for Two", "category": "Fun"})
    return suggestions
