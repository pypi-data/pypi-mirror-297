import json
import logging
import os
from typing import Any
from ..helpers import read_file_content

logger = logging.getLogger(__name__)

class FileOperations:
    def __init__(self, project_abspath: str):
        self.project_abspath = project_abspath

    def manage_files_on_disk(self, arguments: Any):
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
                    if content == '':  # TODO
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

