def calculate_lead_score(source, status, course):
    """
    AI Lead Scoring Algorithm:
    Calculates lead score (0-100) based on source, status, and interest level.
    """
    score = 40  # Base Score

    # 1. Source Weightage
    source_weights = {
        "Walk-in": 30,
        "Phone Call": 25,
        "WhatsApp": 20,
        "Instagram": 15,
        "Facebook": 10,
        "Other": 5
    }
    score += source_weights.get(source, 5)

    # 2. Status Weightage
    status_weights = {
        "Demo Attended": 30,
        "Interested": 20,
        "Contacted": 10,
        "New": 5,
        "Converted": 0,
        "Lost": 0
    }
    score += status_weights.get(status, 0)

    # Cap score at 100
    score = min(score, 100)

    # Priority Assignment
    if score >= 75:
        priority = "High 🔥"
    elif score >= 50:
        priority = "Medium ⚡"
    else:
        priority = "Low ❄️"

    return score, priority