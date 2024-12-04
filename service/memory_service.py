from helper import Logger
from intercepter import post_process_analysis
from model import Memory
from repository import MemoryRepository


class MemoryService:
    def __init__(self):
        self.memory_repository = MemoryRepository()
        self.logger = Logger(__name__)

    @post_process_analysis()
    def save_memory(self, memory: Memory) -> str:
        self.logger.info("Saving memory: %s", memory)
        try:
            return self.memory_repository.save_memory(memory)
        except Exception as e:
            self.logger.error("Error occurred while saving memory: %s", e)
            raise RuntimeError("Error occurred while saving memory") from e

    def get_all_memories(self) -> list[Memory]:
        self.logger.info("Fetching all memories")
        try:
            return self.memory_repository.get_all_memories()
        except Exception as e:
            self.logger.error("Error occurred while fetching all memories: %s", e)
            raise RuntimeError("Error occurred while fetching all memories") from e

    def get_memory_by_id(self, memory_id: str) -> Memory:
        self.logger.info("Fetching memory by id: %s", memory_id)
        try:
            memory = self.memory_repository.get_memory_by_id(memory_id)
            if not memory:
                raise ValueError(f"Memory not found with id: {memory_id}")
            return memory
        except ValueError as ve:
            self.logger.warning("Validation error occurred while fetching memory by id: %s", ve)
            raise
        except Exception as e:
            self.logger.error("Error occurred while fetching memory by id: %s", e)
            raise RuntimeError("Error occurred while fetching memory by id") from e

    @post_process_analysis()
    def update_memory_by_id(self, memory_id: str, memory: Memory) -> int:
        self.logger.info("Updating memory by id: %s", memory_id)
        try:
            existing_memory = self.get_memory_by_id(memory_id)
            if not existing_memory:
                raise ValueError(f"Memory not found with id: {memory_id}")
            return self.memory_repository.update_memory_by_id(memory_id, memory)
        except ValueError as ve:
            self.logger.warning("Validation error occurred while updating memory by id: %s", ve)
            raise
        except Exception as e:
            self.logger.error("Error occurred while updating memory by id: %s", e)
            raise RuntimeError("Error occurred while updating memory by id") from e

    def delete_memory_by_id(self, memory_id: str) -> int:
        self.logger.info("Deleting memory by id: %s", memory_id)
        try:
            memory = self.get_memory_by_id(memory_id)
            if not memory:
                raise ValueError(f"Memory not found with id: {memory_id}")
            return self.memory_repository.delete_memory_by_id(memory_id)
        except ValueError as ve:
            self.logger.warning("Validation error occurred while deleting memory by id: %s", ve)
            raise
        except Exception as e:
            self.logger.error("Error occurred while deleting memory by id: %s", e)
            raise RuntimeError("Error occurred while deleting memory by id") from e

    def get_memories_by_patient_id(self, patient_id: str) -> list[Memory]:
        self.logger.info("Fetching memories by patient id: %s", patient_id)
        try:
            return self.memory_repository.get_memories_by_patient_id(patient_id)
        except Exception as e:
            self.logger.error("Error occurred while fetching memories by patient id: %s", e)
            raise RuntimeError("Error occurred while fetching memories by patient id") from e

    def update_memories(self, memories: list[Memory]) -> None:
        self.logger.info("Updating memories")
        try:
            self.memory_repository.update_memories(memories)
        except Exception as e:
            self.logger.error("Error occurred while updating memories: %s", e)
            raise RuntimeError("Error occurred while updating memories") from e
