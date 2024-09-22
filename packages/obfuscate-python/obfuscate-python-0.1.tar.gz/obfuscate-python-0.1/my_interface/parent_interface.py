# my_interface/parent_interface.py
from abc import ABC, abstractmethod

class ParentInterface(ABC):
    @abstractmethod
    def _hidden_method(self):
        pass

    @abstractmethod
    def public_method(self):
        pass
