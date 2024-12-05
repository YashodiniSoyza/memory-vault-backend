from bson import ObjectId

from config import MongoCollectionConfig
from model import TherapyOutline
from repository import BaseRepository


class TherapyOutlineRepository(BaseRepository):
    def __init__(self):
        super().__init__(MongoCollectionConfig.THERAPY_OUTLINE.value)

    def save_therapy_outline(self, therapy_outline: TherapyOutline) -> str:
        return self.save(therapy_outline.model_dump(by_alias=True))

    def get_therapy_outline_by_id(self, therapy_outline_id: str) -> TherapyOutline:
        result = self.get_one_by_field("_id", ObjectId(therapy_outline_id))
        if result:
            return TherapyOutline(**result)
        else:
            return None

    def update_therapy_outline_by_id(self, therapy_outline_id: str, therapy_outline: TherapyOutline) -> int:
        updated_data = therapy_outline.model_dump(by_alias=True)
        updated_data.pop("_id")
        return self.update({"_id": ObjectId(therapy_outline_id)}, updated_data)

    def get_therapy_outline_by_memory_id(self, memory_id: str) -> TherapyOutline:
        result = self.get_one_by_field("memory_id", memory_id)
        if result:
            return TherapyOutline(**result)
        else:
            return None