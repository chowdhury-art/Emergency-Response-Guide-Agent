from typing import Any, Dict, List


def get_emergency_protocol(
    emergency_type: str,
    severity: str,
    region: str,
    language: str = "en",
) -> str:
    """
    Return a simple, template-based protocol text.

    In a real system this would query curated knowledge bases or APIs.
    For this project, we use basic rule-based templates.
    """

    emergency_type = emergency_type.lower()
    severity = severity.lower()

    if emergency_type == "medical":
        return (
            "If possible, stay calm and ensure the area is safe. "
            "Check if the person is responsive and breathing. "
            "If there is severe bleeding, apply firm pressure with a clean cloth. "
            "Do not give food or drink if the person is unconscious. "
            "Call local emergency services as soon as you can."
        )
    if emergency_type == "fire":
        return (
            "If there is a safe exit, move away from the fire immediately. "
            "Stay low to avoid smoke. "
            "Do not use elevators. "
            "If your clothes catch fire, stop, drop, and roll. "
            "Once safe, call local emergency services."
        )
    if emergency_type == "earthquake":
        return (
            "If you are indoors, drop, cover, and hold on. "
            "Stay away from windows and heavy objects that could fall. "
            "Do not use elevators. "
            "After the shaking stops, carefully move to a safer open area if it is safe to do so. "
            "Check yourself and others for injuries."
        )
    if emergency_type == "flood":
        return (
            "Move to higher ground away from floodwater if you can do so safely. "
            "Avoid walking or driving through moving water. "
            "Do not touch electrical equipment if you are wet or standing in water. "
            "Listen for local alerts and instructions."
        )
    if emergency_type == "storm":
        return (
            "Stay indoors and away from windows. "
            "Secure loose objects outside if there is time and it can be done safely. "
            "Avoid using corded electrical devices during lightning. "
            "Monitor local alerts and be ready to move to a safer location if instructed."
        )

    return (
        "Stay as safe as possible and move away from immediate danger if you can. "
        "Avoid taking unnecessary risks. "
        "Contact local emergency services if you are in danger or unsure what to do."
    )


def get_local_emergency_contacts(region: str) -> Dict[str, Any]:
    """
    Return simple example emergency contact info for a region.
    This is a lightweight, static mapping for demo purposes.
    """
    region_lower = region.lower()

    if any(k in region_lower for k in ["europe", "eu", "germany", "france", "spain", "italy"]):
        return {
            "emergency_number": "112",
            "note": "112 is the general emergency number in many European countries.",
        }
    if any(k in region_lower for k in ["usa", "united states", "america", "canada"]):
        return {
            "emergency_number": "911",
            "note": "911 is the general emergency number in the United States and some other regions.",
        }
    if any(k in region_lower for k in ["uk", "united kingdom", "england", "scotland", "wales"]):
        return {
            "emergency_number": "999",
            "note": "999 is the general emergency number in the UK.",
        }

    return {
        "emergency_number": "local emergency number",
        "note": "Contact your local emergency number. If you are unsure, look for official guidance in your country.",
    }


def get_disaster_alerts(region: str, emergency_type: str) -> List[Dict[str, Any]]:
    """
    Stub for disaster alerts.
    In a real system this might call weather or disaster alert APIs.
    For this project, return a simple mock alert list.
    """
    return [
        {
            "region": region,
            "type": emergency_type,
            "level": "information",
            "message": "Always follow official alerts and instructions from local authorities.",
        }
    ]


def summarize_protocol(text: str, max_steps: int = 7) -> List[str]:
    """
    Heuristic summarizer that splits protocol text into short sentences and truncates.
    This keeps the project simple while still demonstrating a summarization tool.
    """
    if not text:
        return []

    raw_sentences = [s.strip() for s in text.split(".") if s.strip()]
    steps: List[str] = []
    for s in raw_sentences:
        steps.append(s)
        if len(steps) >= max_steps:
            break
    return steps


def compute_risk_score(emergency_type: str, severity: str) -> int:
    """
    Simple rule-based risk scoring.
    Range: 1 (very low) to 10 (very high).
    """
    base = 3

    if emergency_type == "medical":
        base = 7
    elif emergency_type in ["fire", "earthquake", "flood", "storm"]:
        base = 6
    else:
        base = 4

    severity = severity.lower()
    if severity == "low":
        base += 0
    elif severity == "medium":
        base += 1
    elif severity == "high":
        base += 2
    elif severity == "critical":
        base += 3

    if base < 1:
        base = 1
    if base > 10:
        base = 10

    return base
