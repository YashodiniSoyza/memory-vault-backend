from enum import Enum

from pydantic import BaseModel
from typing import List, Optional

from model import Audit


class Education(BaseModel):
    name: str
    year_from: Optional[str] = None
    year_to: Optional[str] = None
    description: Optional[str] = None


class WorkExperience(BaseModel):
    company: str
    position: str
    year_from: Optional[str] = None
    year_to: Optional[str] = None
    description: Optional[str] = None


class MaritalStatus(Enum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"


class WorkStatus(Enum):
    EMPLOYED = "Employed"
    UNEMPLOYED = "Unemployed"
    RETIRED = "Retired"
    STUDENT = "Student"
    HOMEMAKER = "Homemaker"


class FamilyMember(BaseModel):
    name: str
    gender: str
    relation: str
    dob: str
    birth_place: str
    educations: Optional[List[Education]] = None
    work_experiences: Optional[List[WorkExperience]] = None
    current_work_status: Optional[str] = None
    marital_status: Optional[MaritalStatus] = None
    spouse: Optional[str] = None
    children: Optional[List[str]] = None
    notes: Optional[str] = None

    class Config:
        use_enum_values = True


class MedicalRecord(BaseModel):
    condition: str
    date_diagnosed: Optional[str] = None
    ongoing_treatment: Optional[str] = None
    notes: Optional[str] = None


class Patient(Audit):
    name: str
    gender: str
    dob: str
    birth_place: str
    educations: Optional[List[Education]] = None
    work_experiences: Optional[List[WorkExperience]] = None
    current_work_status: Optional[WorkStatus] = None
    marital_status: Optional[MaritalStatus] = None
    family_members: Optional[List[FamilyMember]] = None
    spouse: Optional[str] = None
    children: Optional[List[str]] = None
    grand_children: Optional[List[str]] = None
    caregiver: Optional[str] = None
    medical_history: Optional[List[MedicalRecord]] = None

    class Config:
        use_enum_values = True
