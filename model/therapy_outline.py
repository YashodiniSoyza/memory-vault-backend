from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel


class StepType(Enum):
    INTRODUCTION = "introduction"
    NORMAL = "normal"
    CONCLUSION = "conclusion"


class Script(BaseModel):
    voice: Literal["alloy", "echo", "fable", "onyx", "nova", "shimmer"]
    text: str


class Step(BaseModel):
    step: int
    description: str
    guide: List[str]
    type: StepType
    mediaUrls: List[str]
    script: Script
    audioUrl: Optional[str] = None

    class Config:
        use_enum_values = True


class TherapyOutline(BaseModel):
    patientId: str
    memoryId: str
    status: str
    steps: Optional[List[Step]] = None
