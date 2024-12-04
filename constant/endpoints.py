from enum import Enum


class Endpoints(Enum):
    ROOT = ""

    PATIENT = "/patient"
    BY_PATIENT_ID = "/<patient_id>"

    MEMORY = "/memory"
    BY_MEMORY_ID = "/<memory_id>"

