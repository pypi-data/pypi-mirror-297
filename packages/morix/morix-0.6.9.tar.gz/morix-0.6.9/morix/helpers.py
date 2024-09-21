import os
import subprocess
import threading
import time
from typing import Any, Dict, List
from venv import logger
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from .config_loader import config
import tiktoken


class DotSpinner:
    def __init__(self):
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run)
        reset_terminal()

    def _run(self):
        dot_count = 0
        while not self.stop_event.is_set():
            print('.', end='', flush=True)
            dot_count += 1
            if dot_count >= 15:
                print('\r', end='', flush=True)
                dot_count = 0
            time.sleep(1)

    def start(self):
        if not self.thread.is_alive():
            self.thread.start()

    def stop(self):
        print('\r', end='', flush=True)
        self.stop_event.set()
        self.thread.join(timeout=1)

def reset_terminal():
    subprocess.run(['stty', 'sane'])

def get_string_size_kb(string: str) -> float:
    size_bytes = len(string.encode('utf-8'))
    size_kb = size_bytes / 1024
    return size_kb


def save_response_to_file(response: str, temp_dir: str) -> str:
    count = len(os.listdir(temp_dir)) + 1
    file_path = os.path.join(temp_dir, f"response_{count}.md")
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response)
        logger.info(f"Response saved in {temp_dir}")
    except IOError as e:
        logger.error(f"Error saving response to file: {file_path}: {e}", exc_info=True)
    return file_path


style = Style.from_dict({
    'prompt': 'ansiblue bold',
})


bindings = KeyBindings()

@bindings.add('c-c')
def _(event):
    exit()

@bindings.add('c-t')
def _(event):
    print('\r', end='', flush=True)
    print('Control-T pressed')


@bindings.add('c-d')
def _(event):
    exit()

@bindings.add('enter')
def _(event):
    buffer = event.current_buffer
    if buffer.validate():
        buffer.validate_and_handle()


def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except IOError as e:
        logger.error(f"Failed to read file {file_path}: {e}", exc_info=True)
        return ""

def get_encoding_for_model(model: str = config.gpt_model):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        logger.warning("Model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    return encoding

def tokens_from_messages(messages: List[Dict[str, Any]], ):
    """Returns the number of tokens in messages."""
    num_tokens = 0

    for message in messages:
        num_tokens += tokens_from_message(message)

    return num_tokens

def tokens_from_message(message):
    encoding = get_encoding_for_model()

    def encode_value(value):
        try:
            return len(encoding.encode(str(value), disallowed_special=()))
        except Exception as e:
            logger.error(f"Error encoding value: {value}, Exception: {e}")
            return 0

    if isinstance(message, dict):
        num_tokens = sum(encode_value(value) for value in message.values() if isinstance(value, str))
    else:
        num_tokens = encode_value(message)

    return num_tokens


def check_git_presence(work_folder: str) -> bool:
    if not os.path.exists(os.path.join(work_folder, ".git")):
        return False
    return True


# def merge_functions_describes():
#     try:
#         if os.path.exists(os.path.join(scan_folder, "functions.yml")):
#             project_functions = load_yaml(scan_folder, "functions.yml")
#             merged_functions = config.default_functions + project_functions
#             return merged_functions
#     except Exception as e:
#         logger.error(f"Error loading functions from {scan_folder}: {e}")

#     return config.default_functions

def analize_message(messages):
    m = []
    for message in messages:
        if not hasattr(message, 'role'):
            m.append({ 't' : tokens_from_message(message), 'c' : message['content'] })
        else:
            m.append({ 't' : tokens_from_message(message), 'c' : message.content })
    return m
