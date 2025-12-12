from publisher import WeatherStation
from observers import PhoneDisplay, WindowDisplay 

w = WeatherStation()
pd = PhoneDisplay()
wd = WindowDisplay()
w.attach(pd)
w.attach(wd)

w.update_temp(50)
