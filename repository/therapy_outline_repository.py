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