import json
import logging
import os
import subprocess
import threading
import signal
from typing import Any

from rich.console import Console
from morix import plugin_loader
from morix.scan import get_project_structure
from morix.config_loader import config
from morix.helpers import read_file_content


logger = logging.getLogger(__name__)

plugin_loader = plugin_loader.PluginLoader()
plugin_loader.load_plugins()

console = Console()

class Functions:
    def __init__(self, project_abspath: str):
        self.project_abspath = project_abspath

    def crud_files(self, arguments: Any):
        arguments = json.loads(arguments)
        result = []
        operations = {
            'create': ('created', 'w'),
            'read': ('read', None),
            'update': ('updated', 'w'),
            'delete': ('deleted', None)
        }

        for file in arguments['files']:
            filename = file['filename']
            file_path = os.path.join(self.project_abspath, filename)
            content = file.get('content', '')
            operation = file['operation']

            if operation in operations:
                action, mode = operations[operation]

                if operation == 'create':
                    if content == '':  # Assuming that an empty content means it is a directory
                        os.makedirs(file_path, exist_ok=True)
                        action = 'directory created'
                    else:
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)

                if operation == 'delete':
                    if os.path.exists(file_path):
                        if os.path.isdir(file_path):
                            os.rmdir(file_path)
                        else:
                            os.remove(file_path)
                    else:
                        action = "does not exist"

                if mode and content != '':
                    if not os.path.isdir(file_path):
                        with open(file_path, mode, encoding='utf-8') as f:
                            f.write(content)
                    else:
                        logger.error(f"{filename} is a directory, cannot open it as a file.")
                        result.append(f"{filename}: is a directory, skipped")
                        continue

                if operation == 'read':
                    if not os.path.isdir(file_path):
                        content = read_file_content(file_path)
                    else:
                        content = ""
                        logger.error(f"{filename} is a directory, cannot read it as a file.")
                    result.append(f"{filename}: {content}")
                else:
                    result.append(f"{filename}: {action}")

                logger.info(f"{filename}: {action}")
        return "\n".join(result)

    def run_console_command(self, arguments: Any):
        args = json.loads(arguments)
        command = args['command']
        timeout = args['timeout']

        if not config.permissions.get('allow_run_console_command', False):
            content = "Execution of console commands is not allowed based on the config settings."
            logger.warning(content)
            return content

        console.print(f"[red][bold]Exec:[/bold][/red] {command}\nTimeout: {timeout} seconds")

        def _read_output(process, output_list):
            try:
                for line in process.stdout:
                    print(line, end='')
                    output_list.append(line)
            except Exception as e:
                logger.error(f"Error reading process output: {e}")

        output = []
        err_content = None

        try:
            with subprocess.Popen(
                ['sh', '-c', command],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.project_abspath,
                preexec_fn=os.setsid
            ) as process:

                thread = threading.Thread(target=_read_output, args=(process, output))
                thread.daemon = True
                thread.start()

                try:
                    thread.join(timeout)
                except KeyboardInterrupt:
                    logger.info("Interrupt received, terminating process.")
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    thread.join()
                    raise
                finally:
                    if thread.is_alive():
                        process.kill()
                        thread.join()

        except subprocess.TimeoutExpired:
            err_content = "The command was interrupted due to timeout expiration."
            logger.error(err_content)
        except KeyboardInterrupt:
            err_content = "Process was interrupted by user."
            logger.error(err_content)
        finally:
            output = ''.join(output)
            logger.info(f"Command return code: {process.returncode}")
            max_lines = config.command_output.get('max_output_lines', 100)
            stdout_lines = output.splitlines()[-max_lines:]
            content = "\n".join(stdout_lines)

            if err_content:
                return f"{content}\n{err_content}" if content else err_content
            return content or f"No command execution result received, exit code: {process.returncode}"


    def read_directory_structure(self, arguments: Any):
        args = json.loads(arguments)
        scan_folder = os.path.join(self.project_abspath, args['project'])
        logger.info(f"Reading directory content {scan_folder}")
        return get_project_structure(scan_folder)

    def task_status(self, arguments: Any):
        status = json.loads(arguments)['status']
        if status != 'Completed':
            logger.info(f"Task status {status}")
        return status

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
