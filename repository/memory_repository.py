from typing import List

from config import FirebaseCollectionConfig
from model import Memory
from repository import BaseRepository


class MemoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(FirebaseCollectionConfig.MEMORY.value)

    def save_memory(self, memory: Memory) -> str:
        return self.save(memory.model_dump(by_alias=True))

    def get_all_memories(self) -> List[Memory]:
        result = self.get_all()
        return [Memory(**data) for data in result]

    def get_memory_by_id(self, memory_id: str) -> Memory:
        result = self.get_by_id(memory_id)
        if result:
            return Memory(**result)
        return None

    def update_memory_by_id(self, memory_id: str, memory: Memory):
        updated_data = memory.model_dump(by_alias=True)
        updated_data.pop("id", None)
        return self.update(memory_id, updated_data)

    def delete_memory_by_id(self, memory_id: str):
        return self.delete(memory_id)

    def get_memories_by_patient_id(self, patient_id: str) -> List[Memory]:
        result = self.get_by_field("patientId", patient_id)
        return [Memory(**data) for data in result]

    def update_memories(self, memories: List[Memory]):
        for memory in memories:
            self.update_memory_by_id(memory.id, memory)
