import random
import string
from datetime import datetime, timezone
from typing import Dict


def generate_session_id(length=6) -> str:
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def get_current_utc_date() -> Dict[str, int]:
    now = datetime.now(timezone.utc)
    return {
        "year": now.year,
        "month": now.month,
        "day": now.day,
        "hour": now.hour,
    }


def convert_to_uppercase_underscore(s: str) -> str:
    return s.upper().replace(" ", "_")


def convert_to_lowercase_underscore(s: str) -> str:
    return s.lower().replace(" ", "_")


def convert_to_title_case(s: str) -> str:
    return s.title().replace("_", " ")
