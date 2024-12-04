from typing import Dict, List, Any

from bson import ObjectId
from pymongo import UpdateOne

from config import db


class BaseRepository:

    def __init__(self, collection_name):
        self.collection = db[collection_name]

    @staticmethod
    def collection_exists(collection_name):
        return collection_name in db.list_collection_names()

    def save(self, data):
        result = self.collection.insert_one(data)
        return result.inserted_id

    def save_all(self, data_list):
        result = self.collection.insert_many(data_list)
        return result.inserted_ids

    def update(self, filter, data):
        result = self.collection.update_one(filter, {'$set': data})
        return result.matched_count

    def update_all(self, data_list):
        result = self.collection.update_many(data_list)
        return result.inserted_ids

    def get_all(self):
        result = self.collection.find()
        return list(result)

    def get_list_by_field(self, field, value):
        query = {field: value}
        return list(self.collection.find(query))

    def get_list_by_query(self, query, sort_order=None) -> List[Dict[str, Any]]:
        if sort_order:
            cursor = self.collection.find(query).sort(sort_order)
            return list(cursor)
        return list(self.collection.find(query))

    def get_list_by_query_with_projection(self, query, projection: Dict[str, int] = None) -> List[Dict[str, Any]]:
        if projection is not None:
            return list(self.collection.find(query, projection))
        else:
            return self.get_list_by_query(query)

    def get_one_by_field(self, field, value):
        query = {field: value}
        return self.collection.find_one(query)

    def get_one_by_query(self, query, sort_order=None):
        if sort_order:
            cursor = self.collection.find(query).sort(sort_order).limit(1)
            return cursor.next() if cursor else None
        else:
            return self.collection.find_one(query)

    def get_one_by_query_with_projection(self, query, projection):
        return self.collection.find_one(query, projection)

    def get_one_by_fields(self, fields_values):
        query = fields_values
        return self.collection.find_one(query)

    def get_count_by_fields(self, fields_values):
        query = fields_values
        return self.collection.count_documents(query)

    def get_total_count(self) -> int:
        return self.collection.count_documents({})

    def get_total_count_by_query(self, query) -> int:
        return self.collection.count_documents(query)

    def delete_all(self):
        result = self.collection.delete_many({})
        return result.deleted_count

    def get_by_pagination(self, page: int, page_size: int):
        skip = (page - 1) * page_size
        result = self.collection.find().skip(skip).limit(page_size)
        return list(result)

    def delete_by_query(self, query):
        result = self.collection.delete_many(query)
        return result.deleted_count

    def remove_stale_items(self, scan_id: str):
        result = self.collection.delete_many({
            'request_metadata.id': {'$ne': scan_id}
        })
        return result.deleted_count

    def save_one_with_object_id(self, data: Dict[str, Any]):
        if '_id' in data and isinstance(data['_id'], str):
            data['_id'] = ObjectId(data['_id'])

        filter_ = {'_id': data['_id']}
        update = {'$set': data}
        result = self.collection.update_one(filter_, update, upsert=True)
        return result.matched_count

    def save_all_with_object_id(self, data_list: List[Dict[str, Any]]):
        operations = []
        for info_dict in data_list:
            if '_id' in info_dict and isinstance(info_dict['_id'], str):
                info_dict['_id'] = ObjectId(info_dict['_id'])

            filter_ = {'_id': info_dict['_id']}
            update = {'$set': info_dict}
            operations.append(UpdateOne(filter_, update, upsert=True))

        result = self.collection.bulk_write(operations)
        return result.bulk_api_result
