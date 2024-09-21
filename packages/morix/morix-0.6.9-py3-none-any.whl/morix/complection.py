import logging
import os
import sys
from openai import OpenAI, OpenAIError, RateLimitError, AuthenticationError

from morix.helpers import DotSpinner

from .config_loader import config
from typing import List, Dict, Any

logger = logging.getLogger(__name__)
httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.WARNING)

try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable not set.")
        sys.exit(1)
    client = OpenAI()
except OpenAIError as e:
    logger.critical(f"Error initializing OpenAI client: {e}")
    sys.exit(1)


def chat_completion_request(messages: List[Dict[str, Any]], functions=None) -> Dict:
    """Sends a request to OpenAI."""

    spinner = DotSpinner()
    spinner.start()
    response = None

    try:
        response = client.chat.completions.create(
            model=config.gpt_model,
            messages=messages,
            tools=functions,
            parallel_tool_calls=True,
        )

    except RateLimitError as rle:
        logger.critical(f"Rate limit exceeded: {rle.message}")

    except AuthenticationError as ae:
        logger.critical("Authentication error. Check the API key.")
        exit(1)

    except KeyboardInterrupt:
        logger.info("User interrupted the process.")
        return response

    except Exception as e:
        logger.critical(f"Error generating response from API: {e}")
        logger.debug("Stack trace:", exc_info=True)
        exit(1)

    finally:
        spinner.stop()

    logger.debug("Chat completion request successfully executed.")
    return response
