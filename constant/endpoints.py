from enum import Enum


class Endpoints(Enum):
    ROOT = ""
    PATIENT = "/patient"
    BY_PATIENT_ID = "/<patient_id>"

