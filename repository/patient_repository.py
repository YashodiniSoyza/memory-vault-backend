from typing import List

from bson import ObjectId

from config import MongoCollectionConfig
from model import Status
from model import Patient
from repository import BaseRepository


class PatientRepository(BaseRepository):
    def __init__(self):
        super().__init__(MongoCollectionConfig.PATIENT.value)

    def save_patient(self, patient: Patient) -> str:
        return self.save(patient.model_dump(by_alias=True))

    def get_all_patients(self) -> List[Patient]:
        result = self.get_all()
        return [Patient(**data) for data in result]

    def get_patient_by_id(self, patient_id: str) -> Patient:
        result = self.get_one_by_field("_id", ObjectId(patient_id))
        if result:
            return Patient(**result)
        else:
            return None

    def update_patient_by_id(self, patient_id: str, patient: Patient) -> int:
        updated_data = patient.model_dump(by_alias=True)
        updated_data.pop("_id")
        return self.update({"_id": ObjectId(patient_id)}, updated_data)

    def delete_patient_by_id(self, patient_id: str) -> int:
        return self.update({"_id": ObjectId(patient_id)}, {"status": Status.DELETED.value})
