import os
import yaml
import shutil
import logging
from typing import Dict, Any
from .version import PROGRAM_NAME

logger = logging.getLogger(__name__)

CONFIG_LOCAL_DIR = '../configs'
CONFIG_HOME_DIR = '.config'
CONFIG_YAML = 'config.yml'
CONFIG_FUNCTIONS = 'functions/functions.yml'
CONFIF_IGNORE_FILE = '.gptignore'


def get_config_folder():
    if is_development_mode():
        config_dir = os.path.join(os.path.dirname(__file__), CONFIG_LOCAL_DIR)
    else:
        config_dir = os.path.join(os.path.expanduser('~'), CONFIG_HOME_DIR, PROGRAM_NAME)
    return config_dir


def load_yaml_file(file_path):
    if not os.path.exists(file_path):
        logger.error(f"File not found at path: {file_path}")
        raise FileNotFoundError(f"File not found at path: {file_path}")

    try:
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}", exc_info=True)
        raise


def load_functions(config_dir) -> list:
    functions, functions_files = [], []
    functions_files.append(os.path.join(os.path.dirname(__file__), CONFIG_FUNCTIONS))
    plugins_folder = os.path.join(config_dir, 'plugins')
    if os.path.exists(plugins_folder):
        for file in os.listdir(plugins_folder):
            if file.endswith('.yml'):
                functions_files.append(os.path.join(config_dir, 'plugins', file))

    for function_file in functions_files:
        functions.extend(load_yaml_file(function_file))

    return functions


def load_config() -> Dict[str, Any]:
    config_dir = get_config_folder()
    return load_yaml_file(os.path.join(config_dir, CONFIG_YAML))


def open_config_file() -> None:
    config_path = os.path.join(get_config_folder(), CONFIG_YAML)

    if config_path:
        os.system(f'open "{config_path}"' if os.name == 'posix' else f'start "" "{config_path}"')
    else:
        logger.error("Configuration file not found.")


def is_development_mode() -> bool:
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    res = os.path.isfile(os.path.join(parent_dir, 'setup.py'))
    if res:
        logger.debug("Running in development mode")
    return res

def copy_config_if_not_exist():
    if is_development_mode():
        return
    home_dir = os.path.expanduser('~')
    home_config_dir = os.path.join(home_dir, CONFIG_HOME_DIR, PROGRAM_NAME)
    templates_dir = os.path.join(os.path.dirname(__file__), CONFIG_LOCAL_DIR)
    config_files = []
    for root, dirs, files in os.walk(templates_dir):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            rel_path = os.path.relpath(os.path.join(root, file), templates_dir)
            config_files.append(rel_path)

    if not os.path.exists(home_config_dir):
        os.makedirs(home_config_dir)

    for config_file in config_files:
        template_path = os.path.join(templates_dir, config_file)
        target_path = os.path.join(home_config_dir, config_file)

        if not os.path.exists(template_path):
            continue

        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir, exist_ok=True)

        if not os.path.exists(target_path):
            shutil.copy(template_path, target_path)

    logger.info(f"Configuration copied to {home_config_dir}")


class Config:
    def __init__(self):
        copy_config_if_not_exist()
        self.path = get_config_folder()
        self._config_data = load_yaml_file(os.path.join(self.path, CONFIG_YAML))
        self._console_commands = self._config_data.get('console_commands')
        self._prompt = self._config_data.get('prompt')
        self._scan =  self._config_data.get('scan')
        self.gpt_model = self._config_data.get('gpt_model')
        self.ignore_pattern_files = self._scan.get('ignore_pattern_files')
        self.text_extensions = self._scan.get('text_extensions')
        self.is_wait_for_enter = self._scan.get('wait_enter_before_run', False)
        self.functions = load_functions(self.path)
        self.console_max_output_lines = self._console_commands.get('max_output_lines', 100)
        self.is_console_allow_run = self._console_commands.get('allow_run', False)
        self.role_system_content = self._prompt['system']['content']
        self.additional_user_content = self._prompt['user']['additional_content']
        self.plugins_path = f"{self.path}/plugins"
        self.is_develop_mode = is_development_mode()


config = Config()
