from pydantic import BaseModel
from typing import List, Optional

from enum import Enum

from model import Audit


class MemoryCategory(Enum):
    FAMILY = "family"
    FRIENDS = "friends"
    TRAVEL = "travel"
    WORK = "work"
    ACHIEVEMENTS = "achievements"
    OTHER = "other"


class MemoryEmotion(Enum):
    ANGER = "anger"
    DISGUST = "disgust"
    FEAR = "fear"
    JOY = "joy"
    NEUTRAL = "neutral"
    SADNESS = "sadness"
    SURPRISE = "surprise"


class MediaType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    TEXT = "text"


class Media(BaseModel):
    type: MediaType
    url: Optional[str] = None
    description: str = None

    class Config:
        use_enum_values = True


class Memory(BaseModel):
    id: str
    patientId: str
    title: str
    description: Optional[str] = None
    date: Optional[str] = None
    categories: Optional[List[MemoryCategory]] = None
    emotions: Optional[List[MemoryEmotion]] = None
    media: Optional[List[Media]] = None
    associatedPeople: Optional[List[str]] = None
    tags: Optional[List[str]] = None

    class Config:
        use_enum_values = True
