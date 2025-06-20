from pymongo import MongoClient
from Services.LoggerService import get_logger

logger = get_logger("MCP.DatabaseService")

MONGO_URI = "mongodb://localhost:27017"

class DatabaseService:
    def __init__(self, uri=MONGO_URI):
        self.uri = uri
        self.client = None
        self.db = None

    def connect(self):
        logger.info("Connecting to MongoDB at %s", self.uri)
        self.client = MongoClient(self.uri)
        self.client.admin.command('ping')
        logger.info("Successfully pinged MongoDB server")
        self.db = self.client["mcp"]

    def get_db(self):
        if not self.db:
            self.connect()
        return self.db


def get_database_service():
    return DatabaseService()
