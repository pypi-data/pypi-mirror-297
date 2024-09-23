import json
import subprocess
import logging
import os
import threading
import signal
from typing import Any
from rich.console import Console
from ..settings import config

logger = logging.getLogger(__name__)
console = Console()

class ShellExecutor:
    def __init__(self, project_abspath: str):
        self.project_abspath = project_abspath

    def execute_shell_command(self, arguments: Any):
        args = json.loads(arguments)
        command = args['command']
        timeout = args['timeout']

        if not config.is_console_allow_run:
            content = "Execution of shell commands is not allowed based on the config settings."
            logger.warning(content)
            return content

        console.print(f"[red][bold]Exec:[/bold][/red] {command}\nTimeout: {timeout} seconds")

        if config.is_wait_for_enter:
            input("Press Enter to continue...")

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
            max_lines = config.console_max_output_lines
            stdout_lines = output.splitlines()[-max_lines:]
            content = "\n".join(stdout_lines)

            if err_content:
                return f"{content}\n{err_content}" if content else err_content
            return content or f"No shell command execution result received, exit code: {process.returncode}"
