from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel

from model import Audit


class StepType(Enum):
    INTRODUCTION = "INTRODUCTION"
    NORMAL = "NORMAL"
    CONCLUSION = "CONCLUSION"


class Script(BaseModel):
    voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    text: str


class Step(BaseModel):
    step: int
    description: str
    guide: List[str]
    type: StepType
    media_urls: List[str]
    script: Script
    audio_url: Optional[str] = None

    class Config:
        use_enum_values = True


class TherapyOutline(Audit):
    patient_id: str
    memory_id: str
    steps: List[Step]
