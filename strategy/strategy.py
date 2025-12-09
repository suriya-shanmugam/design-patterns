from abc import ABC, abstractmethod

class RouteStrategy(ABC):
    @abstractmethod
    def build_route(self, a:str, b:str)-> str:
        pass
