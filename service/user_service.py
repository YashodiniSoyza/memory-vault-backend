from helper import Logger
from model.user import User
from repository.user_repository import UserRepository


class UserService:
    def __init__(self):
        self.memory_repository = UserRepository()
        self.logger = Logger(__name__)

    def get_user_by_uid(self, uid: str) -> User:
        self.logger.info("Fetching user by uid: %s", uid)
        try:
            user = self.memory_repository.get_user_by_uid(uid)
            if not user:
                raise ValueError(f"User not found with uid: {uid}")
            return user
        except ValueError as ve:
            self.logger.warning("Validation error occurred while fetching user by uid: %s", ve)
            raise
        except Exception as e:
            self.logger.error("Error occurred while fetching user by uid: %s", e)
            raise RuntimeError("Error occurred while fetching user by uid") from e