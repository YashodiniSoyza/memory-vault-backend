from typing import Optional

from config import FirebaseCollectionConfig
from model import TherapyOutline
from repository import BaseRepository


class TherapyOutlineRepository(BaseRepository):
    def __init__(self):
        super().__init__(FirebaseCollectionConfig.THERAPY_OUTLINE.value)

    def save_therapy_outline(self, therapy_outline: TherapyOutline) -> str:
        return self.save(therapy_outline.model_dump(by_alias=True))

    def get_therapy_outline_by_id(self, therapy_outline_id: str) -> Optional[TherapyOutline]:
        result = self.get_by_id(therapy_outline_id)
        if result:
            return TherapyOutline(**result)
        return None

    def update_therapy_outline_by_id(self, therapy_outline_id: str, therapy_outline: TherapyOutline) -> int:
        updated_data = therapy_outline.model_dump(by_alias=True)
        updated_data.pop("id", None)
        self.update(therapy_outline_id, updated_data)
        return 1

    def get_therapy_outline_by_memory_id(self, memory_id: str) -> Optional[TherapyOutline]:
        result = self.get_by_field("memoryId", memory_id)
        if result:
            return TherapyOutline(**result[0])
        return None
