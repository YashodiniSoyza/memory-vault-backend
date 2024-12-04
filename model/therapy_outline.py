from enum import Enum
from typing import List

from pydantic import BaseModel

from model import Audit


class StepType(Enum):
    INTRODUCTION = "INTRODUCTION"
    NORMAL = "NORMAL"
    CONCLUSION = "CONCLUSION"


class Step(BaseModel):
    step: int
    description: str
    guide: List[str]
    type: StepType
    media_urls: List[str]

    class Config:
        use_enum_values = True


class TherapyOutline(Audit):
    patient_id: str
    memory_id: str
    steps: List[Step]
