HARMFUL_KEYWORDS = [
    "violence", "harm others", "kill", "destroy", "caste supremacy",
    "discrimination", "hatred", "terrorism", "weapon", "bomb"
]

SAFE_MODE_DISCLAIMER = """
⚠️ **Important Disclaimer**:
This is an AI interpretation of Bhagavad Gita teachings, not religious authority.
Please consult qualified spiritual scholars for authoritative guidance.
"""

def check_query_safety(query: str) -> tuple[bool, str]:
    query_lower = query.lower()
    for keyword in HARMFUL_KEYWORDS:
        if keyword in query_lower:
            return False, f"Cannot answer queries promoting {keyword}."
    return True, ""

def format_citation(chapter: int, verse: int, text: str) -> str:
    return f"📿 **Bhagavad Gita {chapter}.{verse}**\n{text}"
