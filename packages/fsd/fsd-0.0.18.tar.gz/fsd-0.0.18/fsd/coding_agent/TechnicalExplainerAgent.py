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

class TechnicalExplainerAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def read_file_content(self, file_path):
        """
        Read and return the content of any type of file, including special files like Podfile.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: Content of the file.
        """
        encodings = ['utf-8', 'iso-8859-1', 'ascii', 'utf-16']
        
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                logger.info(f"Failed to read file {file_path} with {encoding} encoding: {e}")
        
        # If all text encodings fail, try reading as binary
        try:
            with open(file_path, "rb") as file:
                return file.read().decode('utf-8', errors='replace')
        except Exception as e:
            logger.context(f"Failed to read file {file_path} in binary mode: {e}")
        
        return None

    async def get_technical_plan(self, user_prompt, language, role):
        """
        Get a development plan for the given prompt from Azure OpenAI.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.
            language (str): The language in which the response should be provided.
            role (str): The specific role of the engineering specialist.

        Returns:
            str: Development plan or error reason.
        """
        all_file_contents = self.repo.print_summarize_with_tree()
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a senior {role} and explainer engineering specialist. "
                    "Based on the user's request, explain, guide, or provide detailed information to serve in the best way possible.\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Project structure and files overview:\n{all_file_contents}\n\n"
                    f"User request:\n{user_prompt}\n\n"
                    f"You must respond in this language:\n{language}\n\n"
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

    async def get_technical_plans(self, user_prompt, language, role):
        """
        Get development plans based on the user prompt.

        Args:
            user_prompt (str): The user's prompt.

        Returns:
            str: Development plan or error reason.
        """
        
        plan = await self.get_technical_plan(user_prompt, language, role)
        return plan
