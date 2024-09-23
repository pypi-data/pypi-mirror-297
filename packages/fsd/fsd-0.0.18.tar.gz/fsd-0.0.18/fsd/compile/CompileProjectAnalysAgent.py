import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import clean_json
from fsd.util.portkey import AIGateway
from fsd.log.logger_config import get_logger
logger = get_logger(__name__)

class CompileProjectAnalysAgent:
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

        tree_contents = self.repo.print_tree()

        dependency_files_path = self.scan_needed_files(dependency_files)

        all_file_contents = ""
        if dependency_files_path:
            for file_path in dependency_files_path:
                file_content = self.read_file_content(file_path)
                if file_content:
                    all_file_contents += f"\n\nFile: {file_path}:\n{file_content}"
        else:
            all_file_contents = "No dependency files found."

        system_prompt = (
            f"You are a senior DevOps engineer specializing in project compilation and setup. Your task is to analyze the provided project structure and develop a concise, logical plan for setting up and compiling the project for local development using ONLY CLI commands. STRICTLY ADHERE to these guidelines:\n\n"
            f"The correct working project directory: {self.repo.get_repo_path()}\n"
            "1. Provide a SHORT but CLEAR TITLE for the setup and compilation process.\n"
            "2. CAREFULLY ANALYZE the provided project structure.\n"
            "3. If the project structure is empty or missing key files:\n"
               "   a. Start with creating necessary directories and files.\n"
               "   b. Provide CLI commands to create these files with basic content.\n"
               "   c. Then proceed with dependency installation steps.\n"
            "4. If the project structure contains files:\n"
               "   a. CAREFULLY ANALYZE the existing structure, looking for configuration files, build scripts, etc.\n"
               "   b. DO NOT ASSUME the existence of any file not shown in the project structure.\n"
            "5. FOCUS on setup, run, and compile commands for local development environment ONLY.\n"
            f"6. ALWAYS start by navigating to the current working directory with: cd {self.repo.get_repo_path()}\n"
            "7. EXPLAIN each step logically and concisely, referencing the SPECIFIC names and paths of files as they appear in the project structure (or as you create them).\n"
            "8. Provide SPECIFIC CLI commands for setup, file creation (if needed), dependency installation, and compilation using appropriate tools.\n"
            "9. When creating new files, always provide the exact CLI command to create the file and add its content.\n"
            f"10. ALWAYS mention the step to navigate back to the current working directory with: cd {self.repo.get_repo_path()} before each major operation.\n"
            "11. ENSURE each task or command is provided as a separate, logical step, using the EXACT file names and paths as they appear in the project structure (or as you create them).\n"
            "12. ALWAYS follow best practices for dependency management based on the project type:\n"
               "    a. For Python: Use virtual environments and requirements.txt\n"
               "    b. For Node.js: Use package.json and npm/yarn\n"
               "    c. For Java: Use Maven (pom.xml) or Gradle (build.gradle)\n"
               "    d. For Ruby: Use Gemfile and Bundler\n"
               "    e. For other languages: Use appropriate package managers and configuration files\n"
            "13. If dependency configuration files don't exist, CREATE them using CLI commands and add basic content.\n"
            "14. CHECK the project structure CAREFULLY before suggesting any file operations.\n"
               "    If a file or directory doesn't exist, provide CLI commands to create it.\n"
            "15. For compiled languages, include compilation steps. For interpreted languages, ensure the runtime is installed.\n"
            "16. If the project type is unclear, provide steps for multiple potential scenarios.\n"
            "17. When installing dependencies, DO NOT specify any version numbers unless explicitly requested by the user.\n\n"

            "Your response should follow this structure:\n"
            "- Title: [Short, clear title for the setup and compilation process]\n"
            "- Explanation: [Brief explanation of the process, mentioning key steps and files]\n"
            "- Steps: [Numbered list of concise, logical steps with CLI commands, including file creation and content if needed]\n\n"

            "FOCUS on setting up the project based on the provided structure, creating necessary files if they don't exist, and then compiling or running the project. Your plan MUST END with the FINAL COMPILATION or RUN COMMAND for the project.\n\n"

            f"CRITICAL: STRICTLY LIMIT your response to setup and compilation commands for local development ONLY, always starting with 'cd {self.repo.get_repo_path()}' and ENDING with the FINAL COMPILATION or RUN COMMAND. Any deviation from this will be considered a critical error. Only provide deployment-related instructions if explicitly requested by the user. ALWAYS use the EXACT file names and paths as they appear in the provided project structure or as you create them, DO NOT assume the existence of any file not shown in the structure.\n\n"

            "IMPORTANT: Provide each CLI command as a separate step. DO NOT combine multiple commands into a single step."
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
        """
        Get development plan for all txt files from Azure OpenAI based on user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """
        prompt = (
             f"Follow the user prompt strictly and provide a no code response:\n{user_prompt}\n\n"
        )

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = await self.ai.prompt(self.conversation_history, self.max_tokens, 0.2, 0.1)
            return response.choices[0].message.content
        except Exception as e:
            logger.info(f"Failed: {e}")
            return {
                "reason": str(e)
            }


    async def get_idea_plans(self, user_prompt):
        """
        Get development plans for a list of txt files from Azure OpenAI based on user prompt.

        Args:
            files (list): List of file paths.
            user_prompt (str): The user's prompt.

        Returns:
            dict: Development plan or error reason.
        """

        plan = await self.get_idea_plan(user_prompt)
        return plan
