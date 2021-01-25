
from core.Singleton import Singleton
from core.Config import Config
import urllib.request
import json
from datetime import date
import requests
from datetime import datetime,timezone
from dateutil import tz
from core.Logger import Logger

# https://sunrise-sunset.org/api
class SunAPI(metaclass=Singleton):
    def __init__(self):
        self.lat = Config().get()['Position']['Latitude']
        self.lng = Config().get()['Position']['Longitude']
        self.url = "https://api.sunrise-sunset.org/json?lat=%s&lng=%s&date=%s&formatted=0" % (self.lat,
                                                                                             self.lng,
                                                                                             date.today().strftime("%Y-%m-%d")
                                                                                             )
        self.data = None
        self.cacheKey = None
        self.fetch()

    # compare if result contains todays' sunrise
    def valid(self):
        if not self.data:
            return False
        return self.cacheKey == date.today().strftime("%Y-%m-%d")

    def fetch(self):
        if self.valid(): return 1

        r = requests.get(url=self.url)

        self.data = r.json()['results']
        self.cacheKey = date.today().strftime("%Y-%m-%d")

        Logger().logger.info("SunAPI: %s" % self.data)

        return 1

    def isDay(self):
        now = datetime.now(timezone.utc).astimezone(tz.tzlocal())
        return self.UTCDateToLocal(self.data['sunrise']) < now and self.UTCDateToLocal(self.data['sunset']) > now

    def isNight(self):
        return not self.isDay()

    # Expects date as ISO-8601, without tz
    # converts UTC to local date
    def UTCDateToLocal(self, date):
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()

        utc = datetime.utcnow()
        utc = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S+00:00')

        utc = utc.replace(tzinfo=from_zone)
        central = utc.astimezone(to_zone)

        return central
