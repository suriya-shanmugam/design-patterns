from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update_temp(self, temp):
        pass

class PhoneDisplay(Observer):
    
    def update_temp(self, temp):
        print(f"Phone display updated to {temp} temperature")

class WindowDisplay(Observer):
    
    def update_temp(self, temp):
        print(f"Window display updated to {temp} temperature")
