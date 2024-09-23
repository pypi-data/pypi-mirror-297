import logging

from morix.plugin_loader import PluginInterface

logger = logging.getLogger(__name__)

class Plugin(PluginInterface):
    def initialize(self):
        return super().initialize()

    def print_hello_world(self, message):
        print(message)

        return f"mesage '{message}' printed" # REQUIRED response for ai