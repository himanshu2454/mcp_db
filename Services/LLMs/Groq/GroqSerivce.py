import json
import httpx

from Services.LLMs.Groq.Context import GroqContext
from Services.LoggerService import get_logger

logger = get_logger("MCP.GroqService")

GROQ_API_KEY = "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"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

class GroqService:
    def __init__(self):
        self.api_key = GROQ_API_KEY
        self.url = GROQ_URL
        self.model = GROQ_MODEL

    @staticmethod
    def get_context():
        return GroqContext

    async def query(self, messages):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        user_input = messages[0].get("content", "") if messages else ""
        combined_context = f"{self.get_context()}\n\nUser Input: {user_input}"
        payload = {
            "model": GROQ_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": combined_context
                }
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                logger.info("Groq API response: %s", content)
                return json.loads(content)
        except Exception as e:
            logger.error("Groq API error: %s", e)
            return {"response": f"Error querying Groq API: {str(e)}"}

def get_groq_service():
    return GroqService()
