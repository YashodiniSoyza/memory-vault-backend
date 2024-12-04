from bson import ObjectId
from typing import List, Dict
from config import MongoCollectionConfig
from model import Memory
from repository import BaseRepository


class MemoryRepository(BaseRepository):
    def __init__(self):
        super().__init__(MongoCollectionConfig.MEMORY.value)

    def save_memory(self, memory: Memory) -> str:
        return self.save(memory.model_dump(by_alias=True))

    def get_all_memories(self) -> List[Memory]:
        result = self.get_all()
        return [Memory(**data) for data in result]

    def get_memory_by_id(self, memory_id: str) -> Memory:
        result = self.get_one_by_field("_id", ObjectId(memory_id))
        if result:
            return Memory(**result)
        else:
            return None

    def update_memory_by_id(self, memory_id: str, memory: Memory) -> int:
        updated_data = memory.model_dump(by_alias=True)
        updated_data.pop("_id", None)  # Ensure _id is not included in the update
        return self.update({"_id": ObjectId(memory_id)}, updated_data)

    def delete_memory_by_id(self, memory_id: str) -> int:
        return self.update({"_id": ObjectId(memory_id)}, {"status": "DELETED"})

    def get_memories_by_patient_id(self, patient_id: str) -> List[Memory]:
        result = self.get_list_by_field("patient_id", patient_id)
        return [Memory(**data) for data in result]

    def update_memories(self, memories: List[Memory]) -> Dict:
        memory_dicts = [memory.model_dump(by_alias=True) for memory in memories]
        return self.save_all_with_object_id(memory_dicts)
