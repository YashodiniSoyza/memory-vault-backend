from enum import Enum

from pydantic import BaseModel
from typing import List, Optional

from model import Audit


class Education(BaseModel):
    name: str
    yearFrom: Optional[str] = None
    yearTo: Optional[str] = None
    description: Optional[str] = None


class WorkExperience(BaseModel):
    company: str
    position: str
    yearFrom: Optional[str] = None
    yearTo: Optional[str] = None
    description: Optional[str] = None


class MaritalStatus(Enum):
    SINGLE = "MaritalStatus.single"
    MARRIED = "MaritalStatus.married"
    DIVORCED = "MaritalStatus.divorced"
    WIDOWED = "MaritalStatus.widowed"


class WorkStatus(Enum):
    EMPLOYED = "employed"
    UNEMPLOYED = "unemployed"
    RETIRED = "retired"
    STUDENT = "student"
    HOMEMAKER = "homemaker"


class FamilyMember(BaseModel):
    name: str
    gender: str
    relation: str
    dob: str
    birthPlace: Optional[str] = None
    educations: Optional[List[Education]] = None
    workExperiences: Optional[List[WorkExperience]] = None
    currentWorkStatus: Optional[str] = None
    maritalStatus: Optional[MaritalStatus] = None
    spouse: Optional[str] = None
    children: Optional[List[str]] = None
    notes: Optional[str] = None

    class Config:
        use_enum_values = True


class MedicalRecord(BaseModel):
    condition: str
    dateDiagnosed: Optional[str] = None
    ongoingTreatment: Optional[str] = None
    notes: Optional[str] = None


class User(BaseModel):
    uid: str
    email: str
    profilePicUrl: Optional[str] = None
    firstName: str
    lastName: str
    gender: Optional[str]
    dateOfBirth: Optional[str]
    birthPlace: Optional[str]
    educations: Optional[List[Education]] = None
    workExperiences: Optional[List[WorkExperience]] = None
    currentWorkStatus: Optional[WorkStatus] = None
    maritalStatus: Optional[MaritalStatus] = None
    familyMembers: Optional[List[FamilyMember]] = None
    spouse: Optional[str] = None
    children: Optional[List[str]] = None
    grandChildren: Optional[List[str]] = None
    caregiver: Optional[str] = None
    medicalHistory: Optional[List[MedicalRecord]] = None

    class Config:
        use_enum_values = True
