from abc import ABC, abstractmethod

class TextPublisher(ABC):
    @abstractmethod
    def publish(self):
        pass
