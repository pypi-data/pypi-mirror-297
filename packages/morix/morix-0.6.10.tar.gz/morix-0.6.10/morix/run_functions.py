import json
import logging
import os
from typing import Any
from . import plugin_loader
from .scan import get_project_structure
from .functions.file_operations import FileOperations
from .functions.execute_shell_command import ShellExecutor
from .functions.report_task_status import TaskStatusReporter

logger = logging.getLogger(__name__)

plugin_loader = plugin_loader.PluginLoader()
plugin_loader.load_plugins()
class Functions:
    def __init__(self, project_abspath: str):
        self.project_abspath = project_abspath
        self.file_ops = FileOperations(project_abspath)
        self.shell_exec = ShellExecutor(project_abspath)
        self.status = TaskStatusReporter()

    def crud_files(self, arguments: Any):
        return self.file_ops.manage_files_on_disk(arguments)

    def run_console_command(self, arguments: Any):
        return self.shell_exec.execute_shell_command(arguments)

    def task_status(self, arguments: Any):
        return self.status.report_task_status(arguments)

    def read_directory_structure(self, arguments: Any):
        args = json.loads(arguments)
        scan_folder = os.path.join(self.project_abspath, args['project'])
        logger.info(f"Reading directory content {scan_folder}")
        return get_project_structure(scan_folder)


def process_tool_calls(messages, assistant_message: dict, project_abspath: str):
    if not assistant_message.tool_calls:
        return False

    skip_user_question = True
    functions = Functions(project_abspath)

    def message_append(id, name, content):
        messages.append({
            "tool_call_id": id,
            "role": "tool",
            "name": name,
            "content": content,
        })

    for tool in assistant_message.tool_calls:
        function = getattr(functions, tool.function.name, None)
        logger.info(f"Run function '{tool.function.name}'")
        if callable(function):
            content = function(tool.function.arguments)
            message_append(tool.id, tool.function.name, content)
            if tool.function.name == 'task_status' and json.loads(tool.function.arguments)['status'] == 'Completed':
                skip_user_question = False
                logger.info("Task completed")
        else:
            plugin_results = plugin_loader.execute_plugin_function(tool.function.name, json.loads(tool.function.arguments))
            if not plugin_results:
                message_append(tool.id, tool.function.name, "Function does not return any results")
            for result in plugin_results:
                message_append(tool.id, tool.function.name, result)

    return skip_user_question
