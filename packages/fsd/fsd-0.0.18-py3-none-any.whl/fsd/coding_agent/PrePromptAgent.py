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

class PrePromptAgent:
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

    async def get_prePrompt_plan(self, user_prompt):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        all_file_contents = self.repo.print_tree()

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a senior prompt engineering specialist. Analyze the provided project files and the user's prompt and respond in JSON format. Follow these guidelines:\n\n"
                    "original_prompt_language: Determine the user's main prompt language such as English, Vietnamese, Indian, etc.\n"
                    "role: Choose a specific single type of engineer role that best fits to complete the user's request for this project.\n"
                    "processed_prompt: If the user's original prompt is not in English, translate it to English. Correct grammar, ensure it is clear, concise, and based on current project insights. Make sure it's descriptive to help coding agent build easier.\n"
                    "pipeline: You need to pick the best pipeline that fits the user's prompt. Only respond with a number for the specific pipeline you pick, such as 1, 2, 3, 4, 5, 6 following the guidelines below:\n"
                    "If the user requires a task you can perform, use the options below:\n"
                    "1. Compile error: Use only if compile errors occur.\n"
                    "2. Create/add files or folders: Use if the user only asks to add/create new files or folders.\n"
                    "3. Move files or folders: Use if the user only asks to move files or folders.\n"
                    "4. Format code: Use if user ask for refactoring, formatting code, writing file comments, or anything related to code formatting.\n"
                    "5. Main coding agent: Use for more complex tasks that require building or significantly altering functionality, fixing non-compile error bugs (such as performance issues or fatal errors), or developing new features or applications. This pipeline is for situations where a development plan is necessary before coding, such as when writing a new app, creating intricate functionalities, or performing extensive bug fixes. It should also be used if the task involves adding new files or modules to the project.\n"
                    "The JSON response must follow this format:\n\n"
                    "{\n"
                    '    "processed_prompt": "",\n'
                    '    "role": "",\n'
                    '    "pipeline": "1 or 2 or 3 or 4 or 5",\n'
                    '    "original_prompt_language": "",\n'
                    "}\n\n"
                    "Return only a valid JSON response without additional text or Markdown symbols."
                )
            },
            {
                "role": "user",
                "content": (
                    f"User original prompt:\n{user_prompt}\n\n"
                    f"Here are the current project structure and files summary:\n{all_file_contents}\n"
                )
            }
        ]

        try:
            response = await self.ai.prompt(messages, self.max_tokens, 0.2, 0.1)
            res = json.loads(response.choices[0].message.content)
            return res
        except json.JSONDecodeError:
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            return plan_json
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }

    async def get_prePrompt_plans(self, user_prompt):
        plan = await self.get_prePrompt_plan(user_prompt)
        logger.info(f"Completed preparing for: {user_prompt}")
        return plan
