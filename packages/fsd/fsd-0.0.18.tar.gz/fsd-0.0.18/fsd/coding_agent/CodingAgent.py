import os
import sys
import asyncio
from datetime import datetime
import aiohttp
import json
import re
from json_repair import repair_json

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import get_current_time_formatted, clean_json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CodingAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.conversation_history = []
        self.ai = AIGateway('bedrock')

    def get_current_time_formatted(self):
        """Return the current time formatted as mm/dd/yy."""
        current_time = datetime.now()
        formatted_time = current_time.strftime("%m/%d/%y")
        return formatted_time

    def initial_setup(self, context_files, instructions, context, role, crawl_logs):
        """Initialize the setup with the provided instructions and context."""

        prompt = f"""You are a senior {role} working as a coding agent. You will receive detailed instructions to work on. Follow these guidelines strictly:
                **Response Guidelines:**
                1. For ALL code changes, additions, or deletions, you MUST ALWAYS use the following *SEARCH/REPLACE block* format:

                   <<<<<<< SEARCH
                   [Existing code to be replaced, if any]
                   =======
                   [New or modified code]
                   >>>>>>> REPLACE

                2. For new code additions, use an empty SEARCH section:

                   <<<<<<< SEARCH
                   =======
                   [New code to be added]
                   >>>>>>> REPLACE

                3. Ensure that the SEARCH section exactly matches the existing code, including whitespace and comments.

                4. For large files, focus on the relevant sections. Use comments to indicate skipped portions:
                   // ... existing code ...

                5. For complex changes or large files, break them into multiple SEARCH/REPLACE blocks.

                6. CRITICAL: NEVER provide code snippets, suggestions, or examples outside of the SEARCH/REPLACE block format. ALL code must be within these blocks.

                7. Do not provide explanations, ask questions, or engage in discussions. Only return SEARCH/REPLACE blocks.

                8. If a user's request cannot be addressed solely through SEARCH/REPLACE blocks, do not respond.

                **Code Guidelines:**
                9. Implement robust error handling with try-except blocks where appropriate. Use logging (e.g., self.logger.error(), self.logger.info()) for important events and errors.

                10. Create modular code with clear separation of concerns. Use classes, functions, and methods with single responsibilities. Implement inheritance, composition, and interfaces where appropriate.

                11. Optimize for performance using efficient algorithms and data structures. Consider caching mechanisms for frequently accessed data. Use asynchronous programming (async/await) for I/O-bound operations.

                12. For UI components, implement responsive designs using flexbox or grid layouts. Ensure accessibility with proper ARIA attributes and semantic HTML.

                13. Write comprehensive docstrings for classes and functions. Use clear, descriptive variable and function names. Include inline comments for complex logic.

                14. Implement input validation and sanitization. Use parameterized queries for database operations. Implement proper authentication and authorization checks.

                15. Use environment variables for configuration. Implement localization support using i18n libraries. Ensure code works across different operating systems.

                16. Follow existing code structure and naming conventions. Use dependency injection for better testability and loose coupling.

                17. Utilize existing project dependencies. If new ones are absolutely necessary, clearly state the reason and provide installation instructions.

                18. Implement unit tests for new functions and methods. Ensure test coverage for critical paths.

                19. Optimize imports and remove unused ones. Use absolute imports for better maintainability.

                20. Implement proper memory management, especially for resource-intensive operations.

                21. Use type hints and docstring type annotations for better code readability and IDE support.

                22. Implement appropriate design patterns (e.g., Factory, Singleton, Observer) where they improve code structure and maintainability.

                Remember, your responses should ONLY contain SEARCH/REPLACE blocks for code changes. Nothing else is allowed.
        """

        self.conversation_history = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"These are your instructions: {instructions} and the current context: {context}"},
            {"role": "assistant", "content": "Got it!"}
        ]

        if context_files:
            all_file_contents = ""

            files = self.scan_needed_files(context_files)

            for file_path in files:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}\n{file_content}"

            self.conversation_history.append({"role": "user", "content": f"These are all the supported files to provide enough context for this task: {all_file_contents}"})
            self.conversation_history.append({"role": "assistant", "content": "Got it!"})

        if crawl_logs:
            self.conversation_history.append({"role": "user", "content": f"This task requires you to scrape data. Here is the provided data: {crawl_logs}"})
            self.conversation_history.append({"role": "assistant", "content": "Got it!"})

    def scan_for_single_file(self, filename):
        """
        Scan for a single specified file in the specified directory.

        Args:
            filename (str): The name of the file to look for.

        Returns:
            str: Path to the specified file if found, else None.
        """
        if not os.path.exists(self.repo.get_repo_path()):
            logger.debug(f"Directory does not exist: {self.repo.get_repo_path()}")
            return None

        for root, _, files in os.walk(self.repo.get_repo_path()):
            if filename in files:
                return os.path.join(root, filename)

        return None

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

        return found_files

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

        # Start of Selection

    async def get_coding_request(self, is_first, file, techStack):
            """
            Get coding response for the given instruction and context from Azure OpenAI.

            Args:
                session (aiohttp.ClientSession): The aiohttp session to use for the request.
                is_first (bool): Flag to indicate if it's the first request.
                prompt (str): The coding task prompt.
                file (str): Name of the file to work on.
                techStack (str): The technology stack for which the code should be written.

            Returns:
                dict: The code response or error reason.

            file_path = self.scan_for_single_file(file)
            context = self.read_file_content(file_path)
            tree_context = self.read_file_content(tree[0])
            """

            file_path = self.scan_for_single_file(file)
            context = self.read_file_content(file_path)

            user_prompt = (
                f"{'Begin' if is_first else 'Continue'} implementing the following task on {file}:\n"
                #f"Current file context: {context}\n"
                f"Adhere to these enterprise-level coding guidelines:\n"
                f"1. Strictly follow {techStack} syntax, best practices, and design patterns. Ensure code is idiomatic and leverages language-specific features effectively.\n"
                f"Your response must exclusively contain SEARCH/REPLACE blocks for code changes. Provide complete implementations, not placeholders. Do not include any other content outside these blocks."
            )

            self.conversation_history.append({"role": "user", "content": user_prompt})

            try:
                response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
                self.conversation_history.append({"role": "assistant", "content": response.choices[0].message.content})
                return response.choices[0].message.content
            except Exception as e:
                logger.info(f"Failed: {e}")
                return {
                    "reason": str(e)
                }


    async def get_coding_requests(self, is_first, file, techStack):
        """
        Get coding responses for a list of files from Azure OpenAI based on user instruction.

        Args:
            is_first (bool): Flag to indicate if it's the first request.
            prompt (str): The coding task prompt.
            file (str): Name of the file to work on.
            techStack (str): The technology stack for which the code should be written.

        Returns:
            dict: The code response or error reason.
        """
        return await self.get_coding_request(is_first, file, techStack)

    def clear_conversation_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
