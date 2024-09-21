from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def initialize(self):
        pass