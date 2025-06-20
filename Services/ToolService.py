from Services.DatabaseService import get_db
from Services.LoggerService import get_logger

logger = get_logger("MCP.ToolService")

class ToolService:
    def __init__(self, db=None):
        self.db = db if db is not None else get_db()
        self.module_collection = self.db["modules"]

    def db_call(self, query, user_prompt=""):
        try:
            if user_prompt and "count" in user_prompt.lower():
                count = self.module_collection.count_documents(query)
                return f"Count: {count}"
            modules = self.module_collection.find(query)
            modules_list = list(modules)
            logger.info("Database query result: %s", modules_list)
            return modules_list  # Return raw data
        except Exception as e:
            logger.error("Error executing db_call: %s", e)
            return f"Failed to execute query: {str(e)}"

def get_tool_service():
    db = get_db()
    return ToolService(db)