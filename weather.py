import pyowm
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config

owm = pyowm.OWM('0a678ea48ded23352899115ec98b99c3')
config_dict = get_default_config()
config_dict['language'] = 'ru'
mgr = owm.weather_manager()

observation = mgr.weather_at_place('Krasnodar,RU')
w = observation.weather

def getStatus():
    return w.detailed_status

def getSpeed():
    return w.wind()['speed']

def getHumidity():
    return w.humidity

def getTemp():
    return int(w.temperature("celsius")["temp_max"])

def getRain():
    return w.rain