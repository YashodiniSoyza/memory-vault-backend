from helper import Logger
from model import Patient
from repository import PatientRepository


class PatientService:
    def __init__(self):
        self.patient_repository = PatientRepository()
        self.logger = Logger(__name__)

    def save_patient(self, patient: Patient) -> str:
        self.logger.info("Saving patient: %s", patient)
        try:
            return self.patient_repository.save_patient(patient)
        except Exception as e:
            self.logger.error("Error occurred while saving patient: %s", e)
            raise RuntimeError("Error occurred while saving patient") from e

    def get_all_patients(self) -> list[Patient]:
        self.logger.info("Fetching all patients")
        try:
            return self.patient_repository.get_all_patients()
        except Exception as e:
            self.logger.error("Error occurred while fetching all patients: %s", e)
            raise RuntimeError("Error occurred while fetching all patients") from e

    def get_patient_by_id(self, patient_id: str) -> Patient:
        self.logger.info("Fetching patient by id: %s", patient_id)
        try:
            patient = self.patient_repository.get_patient_by_id(patient_id)
            if not patient:
                raise ValueError("Patient not found with id: %s", patient_id)
            return patient
        except ValueError as ve:
            self.logger.warning("Validation error occurred while fetching patient by id: %s", ve)
            raise
        except Exception as e:
            self.logger.error("Error occurred while fetching patient by id: %s", e)
            raise RuntimeError("Error occurred while fetching patient by id") from e

    def update_patient_by_id(self, patient_id: str, patient: Patient) -> int:
        self.logger.info("Updating patient by id: %s", patient_id)
        try:
            existing_patient = self.get_patient_by_id(patient_id)
            if not existing_patient:
                raise ValueError("Patient not found with id: %s", patient_id)
            return self.patient_repository.update_patient_by_id(patient_id, patient)
        except ValueError as ve:
            self.logger.warning("Validation error occurred while updating patient by id: %s", ve)
            raise
        except Exception as e:
            self.logger.error("Error occurred while updating patient by id: %s", e)
            raise RuntimeError("Error occurred while updating patient by id") from e

    def delete_patient_by_id(self, patient_id: str) -> int:
        try:
            patient = self.get_patient_by_id(patient_id)
            if not patient:
                raise ValueError("Patient not found with id: %s", patient_id)
            return self.patient_repository.delete_patient_by_id(patient_id)
        except ValueError as ve:
            self.logger.warning("Validation error occurred while deleting patient by id: %s", ve)
            raise
        except Exception as e:
            self.logger.error("Error occurred while deleting patient by id: %s", e)
            raise RuntimeError("Error occurred while deleting patient by id") from e
