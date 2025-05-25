from threading import Thread

from helper import Logger
from model import Memory
from model.user import User
from service import MediaDescriptionAnalysisService, UserService, MemoryService, TherapyOutlineService, \
    TherapyVoiceGenerationService


class TherapyGenerationService:
    def __init__(self):
        self.user_service = UserService()
        self.memory_service = MemoryService()
        self.therapy_outline_service = TherapyOutlineService()
        self.therapy_voice_generation_service = TherapyVoiceGenerationService()
        self.logger = Logger(__name__)

    def generate_therapy(self, memory_id: str):
        self.logger.info("Starting therapy generation for memory: %s", memory_id)
        try:
            memory = self.memory_service.get_memory_by_id(memory_id)
            if not memory:
                raise ValueError(f"No memory found with ID: {memory_id}")

            user = self.user_service.get_user_by_uid(memory.patientId)
            if not user:
                raise ValueError(f"No user found with ID: {memory.patientId}")

            therapy_id = self.therapy_outline_service.save_therapy_outline(user.uid, memory_id)

            thread = Thread(target=self.start_therapy_generation, args=(user, memory, therapy_id),
                            name=f"TherapyGenerationThread-{memory_id}")
            thread.start()
        except Exception as e:
            self.logger.error("Error occurred while generating therapy: %s", e)
            raise RuntimeError("Error occurred while generating therapy") from e

    def start_therapy_generation(self, user: User, memory: Memory, therapy_id: str):
        try:
            self.therapy_outline_service.update_therapy_outline(therapy_id, user.uid, memory.id, status="processing")

            media_description_analysis_service = MediaDescriptionAnalysisService()
            media_description_analysis_service.analyze_memories_by_patient_id(user.uid)

            self.therapy_outline_service.generate_and_save_therapy_outline(memory, user, therapy_id)

            self.therapy_voice_generation_service.generate_voice_for_therapy_outline(therapy_id)
            self.logger.info("Therapy generation completed for memory: %s", memory.id)
        except Exception as e:
            self.logger.error("Error occurred while updating therapy outline status: %s", e)
            self.therapy_outline_service.update_therapy_outline(therapy_id, user.uid, memory.id, status="failed")
            raise RuntimeError("Error occurred while updating therapy outline status") from e
