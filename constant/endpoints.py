from enum import Enum


class Endpoints(Enum):
    ROOT = ""

    PATIENT = "/patient"
    BY_PATIENT_ID = "/<patient_id>"
    BY_USER_ID = "/<user_id>"

    MEMORY = "/memory"
    BY_MEMORY_ID = "/<memory_id>"

    THERAPY = "/therapy"
    GENERATE_THERAPY = "/process/<memory_id>"
    BY_THERAPY_ID = "/<therapy_id>"

