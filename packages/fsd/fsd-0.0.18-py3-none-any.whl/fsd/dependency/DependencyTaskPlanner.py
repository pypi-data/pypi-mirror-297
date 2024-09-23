import os
import aiohttp
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fsd.util.utils import clean_json
from fsd.util.portkey import AIGateway
from json_repair import repair_json
from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

class DependencyTaskPlanner:
    """
    A class to plan and manage tasks using AI-powered assistance.
    """

    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    async def get_task_plan(self, instruction, os_architecture):
        """
        Get a dependency installation plan based on the user's instruction using AI.

        Args:
            instruction (str): The user's instruction for dependency installation planning.
            os_architecture (str): The operating system and architecture of the target environment.

        Returns:
            dict: Dependency installation plan or error reason.
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a principal-level DevOps engineer tasked with creating a focused, step-by-step dependency installation plan. Your goal is to structure tasks logically, following a pyramid architecture approach:\n\n"
                    f"The correct working project directory: {self.repo.get_repo_path()}\n"
                    "1. Always start with a task to navigate to the project directory.\n"
                    "2. Carefully analyze the provided project tree structure before suggesting any file operations.\n"
                    "3. If a configuration file doesn't exist, include separate steps to create it using CLI commands (e.g., 'touch' to create the file, then 'echo' to add content).\n"
                    "4. Organize installation steps based on the pyramid architecture principle, starting with foundational components.\n"
                    "5. Consider the provided OS architecture when specifying commands.\n"
                    "6. Provide detailed, environment-specific commands that can be executed directly in a terminal.\n"
                    "7. Strictly focus on dependency configuration and installation. Do not include any steps for writing application code, opening projects, downloading files, or tasks unrelated to dependency management.\n"
                    "8. Ensure each task or command is provided as a separate step. Never combine multiple commands into a single step.\n"
                    "9. Do not include steps to check versions or file existence, as these cannot be determined from the provided tree structure.\n"
                    "10. When installing dependencies, DO NOT specify any version numbers unless explicitly requested by the user.\n\n"
                    "For each task, provide:\n"
                    "- file_name: The dependency configuration file to be updated (if applicable), or 'N/A' for bash commands.\n"
                    "- prompt: A specific, comprehensive instruction for the given dependency-related task. For 'update' method, include detailed configuration changes, such as specific pods to add (e.g., 'Add the following pod: pod 'Firebase/Core').\n"
                    "- method: Either 'update' for build file modifications or 'bash' for terminal commands.\n"
                    "- command: The exact command to be executed (for 'bash' method only). Each command should be a single operation.\n\n"
                    "Respond with a valid JSON in this format:\n"
                    "{\n"
                    '    "steps": [\n'
                    '        {\n'
                    '            "file_name": "N/A",\n'
                    '            "prompt": "Navigate to the project directory",\n'
                    '            "method": "bash",\n'
                    f'            "command": "cd {self.repo.get_repo_path()}"\n'
                    '        },\n'
                    '        {\n'
                    '            "file_name": "",\n'
                    '            "prompt": "",\n'
                    '            "method": "",\n'
                    '            "command": ""\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "Provide only the JSON response without additional text or Markdown symbols. Remember to separate each step, such as using 'touch' before 'echo' when creating and adding content to files."
                )
            },
            {
                "role": "user",
                "content": f"Create a focused, step-by-step dependency installation plan following the pyramid architecture for these instructions. Consider the OS architecture: {os_architecture}. Provide detailed, environment-specific commands. Only include steps related to dependency configuration and installation. Do not include any steps for opening files, projects, or downloading. Ensure each task or command is provided as a separate step, separating operations like file creation and content addition. Do not specify any version numbers when installing dependencies unless explicitly requested. Here's the current project tree structure:\n\n{self.repo.print_tree()}\n\nBased on this structure, create the installation plan for:\n{instruction}\n"
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
            logger.error(f"Failed to get task plan: {e}")
            return {"reason": str(e)}

    async def get_task_plans(self, instruction):
        plan = await self.get_task_plan(instruction)
        return plan
