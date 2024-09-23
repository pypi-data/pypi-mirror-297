import json
import logging
from typing import Any

logger = logging.getLogger(__name__)

class TaskStatusReporter:
    def report_task_status(self, arguments: Any):
        status = json.loads(arguments)['status']
        if status != 'Completed':
            logger.info(f"Task status {status}")
        return status
