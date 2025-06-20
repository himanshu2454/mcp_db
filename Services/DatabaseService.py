from pymongo import MongoClient
from Services.LoggerService import get_logger

logger = get_logger("MCP.DatabaseService")

MONGO_URI = "mongodb://localhost:27017"

def get_db():
    logger.info("Connecting to MongoDB at %s", MONGO_URI)
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    logger.info("Successfully pinged MongoDB server")
    db = client["mcp"]
    return db
