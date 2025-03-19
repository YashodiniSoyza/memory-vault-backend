from typing import Dict, List, Any
from config import db


class BaseRepository:
    def __init__(self, collection_name):
        self.collection = db.collection(collection_name)

    def save(self, data: Dict[str, Any]) -> str:
        _, ref = self.collection.add(data)
        return ref.id

    def save_all(self, data_list: List[Dict[str, Any]]):
        batch = db.batch()
        for data in data_list:
            doc_ref = self.collection.document()  # Automatically generate a new doc ID
            batch.set(doc_ref, data)
        batch.commit()

    def update(self, doc_id: str, data: Dict[str, Any]):
        doc_ref = self.collection.document(doc_id)
        doc_ref.update(data)

    def get_all(self) -> List[Dict[str, Any]]:
        docs = self.collection.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    def get_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        query = self.collection.where(field, "==", value)
        docs = query.stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    def get_by_id(self, doc_id: str) -> Dict[str, Any]:
        doc_ref = self.collection.document(doc_id)
        doc = doc_ref.get()
        if doc.exists:
            return {"id": doc.id, **doc.to_dict()}
        return None

    def delete(self, doc_id: str):
        doc_ref = self.collection.document(doc_id)
        doc_ref.delete()
