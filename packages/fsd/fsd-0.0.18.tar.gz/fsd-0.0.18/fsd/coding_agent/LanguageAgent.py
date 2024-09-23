import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import clean_json
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class LanguageAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_language_plan(self, user_prompt, role):
        """
        Get a development plan for the given prompt from Azure OpenAI.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.

        Returns:
            str: Development plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a senior {role} and prompt engineering specialist. "
                    "If the user's original prompt is not in English, translate it to 100% English. "
                    "Correct grammar, ensure it is clear and concise. Keep it crisp and short, avoiding confusion."
                )
            },
            {
                "role": "user",
                "content": (
                    f"User original prompt:\n{user_prompt}\n\n"
                )
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            return response.choices[0].message.content
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }

    async def get_language_plans(self, user_prompt, role):
        plan = await self.get_language_plan(user_prompt, role)
        return plan
