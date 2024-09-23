import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import clean_json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
from json_repair import repair_json
logger = get_logger(__name__)

class DependencyProjectAnalysForCodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []

    def remove_latest_conversation(self):
        """Remove the latest conversation from the history."""
        if self.conversation_history:
            self.conversation_history.pop()

    def initial_setup(self, dependency_files, OS_architecture):
        """
        Initialize the conversation with a system prompt and user context.
        """

        all_file_contents = ""
        tree_contents = self.repo.print_tree()

        dependency_files_path = self.scan_needed_files(dependency_files)

        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"You are a senior DevOps engineer specializing in dependency management. Your task is to analyze the provided project files and develop a comprehensive dependency installation plan using EXCLUSIVELY CLI commands. STRICTLY ADHERE to these guidelines:\n\n"
            f"The correct working project directory: {self.repo.get_repo_path()}\n"
            "1. METICULOUSLY analyze the provided tree structure and identify ALL dependencies.\n"
            "2. CAREFULLY EXAMINE the tree structure before suggesting any file operations.\n"
            "3. If dependency files (such as requirements.txt, package.json, Podfile, etc.) DO NOT exist in the tree structure, EXPLICITLY state this and provide CLI commands to create them, including the FULL PATH where they should be added.\n"
            "4. DO NOT ASSUME the existence of any files or directories not explicitly shown in the tree structure.\n"
            "5. If installation is needed, provide a detailed plan following these steps:\n"
            f"   a. ALWAYS start by navigating to the current working directory with: cd {self.repo.get_repo_path()}\n"
            "   b. Set up a virtual environment if needed (e.g., for Python projects).\n"
            "   c. Create a requirements.txt file if it doesn't exist and list ALL required dependencies.\n"
            "   d. Provide SPECIFIC CLI installation commands using ONLY command-line package managers.\n"
            "   e. Create necessary directory structures and files if needed, based SOLELY on the provided tree structure.\n"
            "   f. For projects starting from scratch, set up dependency management based on the identified technology stack and OS architecture.\n"
            f"6. ALWAYS navigate back to the current working directory with: cd {self.repo.get_repo_path()} before each major operation.\n"
            "7. Provide each task or command as a separate step.\n"
            "8. For iOS projects, use CocoaPods CLI commands instead of Swift Package Manager.\n"
            "9. FOCUS SOLELY on dependency installation and management. DO NOT include steps for opening projects, writing code, or actions beyond dependency setup.\n"
            "10. ENSURE all commands are compatible with the provided OS architecture.\n"
            "11. DO NOT include steps for integrating or configuring installed dependencies within the project.\n"
            "12. NEVER specify versions when installing dependencies unless explicitly requested by the user.\n"
            "13. DO NOT include steps to check versions or file existence, as these cannot be determined from the provided tree structure.\n"
            "14. Prioritize compatibility when selecting dependencies, ensuring they work well together and with the existing system.\n"
            "15. If no dependency files exist, use CLI commands to create them and add necessary dependencies.\n"
            "16. ALWAYS separate each step, such as using 'touch' before 'echo' when creating and populating files.\n\n"

            "Your response MUST be a FLAWLESSLY formatted JSON object, DEVOID of ANY extraneous text, comments, or markdown elements. The JSON response MUST STRICTLY adhere to one of these structures, with ABSOLUTELY NO DEVIATIONS:\n\n"
            "If installation is not needed or possible:\n"
            "{\n"
            '    "should_process_install_dependency": false,\n'
            '    "reason": "Brief explanation why installation is not needed or possible"\n'
            "}\n\n"

            "If installation is needed:\n"
            "{\n"
            '    "should_process_install_dependency": true,\n'
            '    "plan": "Detailed dependency installation plan following the guidelines"\n'
            "}\n\n"

            "Ensure 'should_process_install_dependency' is a valid Python boolean (true or false).\n"
            f"CRITICAL: STRICTLY LIMIT your response to the JSON object. Any deviation will be considered a critical error."
        )

        self.conversation_history.append({"role": "system", "content": system_prompt})
        self.conversation_history.append({"role": "user", "content":  f"Here are the current dependency files: {all_file_contents}\n\nProject structure: {tree_contents}\n\nOS Architecture: {OS_architecture}"})
        self.conversation_history.append({"role": "assistant", "content": "Got it! Give me user prompt so i can support them."})

    def scan_needed_files(self, filenames):
        """
        Scan for specified files in the specified directory.

        Args:
            filenames (list): List of filenames to look for.

        Returns:
            list: Paths to the specified files if found.
        """
        found_files = []

        if not os.path.exists(self.repo.get_repo_path()):
            logger.debug(f"Directory does not exist: {self.repo.get_repo_path()}")
            return found_files

        for root, _, files in os.walk(self.repo.get_repo_path()):
            for filename in filenames:
                if filename in files:
                    file_path = os.path.join(root, filename)
                    found_files.append(file_path)

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

    async def get_idea_plan(self, user_prompt):
        prompt = (
            f"Based on the user prompt, return a JSON object with the following structure:\n"
             f"Correct project directory: {self.repo.get_repo_path()}\n"
            "If installation is not needed or possible:\n"
            "{\n"
            '    "should_process_install_dependency": false,\n'
            '    "reason": "Brief explanation why installation is not needed or possible"\n'
            "}\n\n"
            "If installation is needed:\n"
            "{\n"
            '    "should_process_install_dependency": true,\n'
            '    "plan": "Detailed dependency installation plan following the guidelines"\n'
            "}\n\n"
            "Ensure 'should_process_install_dependency' is a valid Python boolean (true or false).\n"
            f"User prompt: {user_prompt}\n\n"
            "Your response MUST be a FLAWLESSLY formatted JSON object, DEVOID of ANY extraneous text, comments, or markdown elements."
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
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


    async def get_idea_plans(self, user_prompt):
        plan = await self.get_idea_plan(user_prompt)
        return plan
