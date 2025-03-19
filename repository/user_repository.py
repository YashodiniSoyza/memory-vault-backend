from config import FirebaseCollectionConfig
from model.user import User
from repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(FirebaseCollectionConfig.USERS.value)

    def get_user_by_uid(self, uid: str):
        result = self.get_by_field("uid", uid)
        if result:
            return User(**result[0])
        return None
