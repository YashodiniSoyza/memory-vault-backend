from pymongo import MongoClient
import os
from dotenv import load_dotenv

from constant import EnvKeys

load_dotenv()

client = MongoClient(os.getenv(EnvKeys.MONGO_URI.value))
db = client[os.getenv(EnvKeys.DATABASE_NAME.value)]
