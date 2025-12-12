from observers import Observer

class WeatherStation :
    def __init__(self):
        self.temp = 0
        self._observers = []
    
    def attach(self, observer : Observer):
        self._observers.append(observer)

    def detach(self, observer : Observer):
        self._observers.remove(observer)

    def update_temp(self, temp):
        self.temp = temp
        self.notify()

    def notify(self):
        for observer in self._observers :
            observer.update_temp(self.temp)

