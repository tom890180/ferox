
from core.Singleton import Singleton
from core.Config import Config
import urllib.request
import json
import requests
from datetime import datetime,timezone,date
from dateutil import tz
from core.Logger import Logger

# https://sunrise-sunset.org/api
class SunAPI(metaclass=Singleton):
    def __init__(self):
        self.lat = Config().get()['Position']['Latitude']
        self.lng = Config().get()['Position']['Longitude']
        self.url = "https://api.sunrise-sunset.org/json?lat=%s&lng=%s&date=%s&formatted=0" % (self.lat,
                                                                                             self.lng,
                                                                                             self.getTodayAsUTC().strftime("%Y-%m-%d")
                                                                                             )
        self.data = None
        self.cacheKey = None
        self.fetch()

    # compare if result contains todays' sunrise
    def valid(self):
        return self.cacheKey == self.getTodayAsUTC().strftime("%Y-%m-%d")

    def fetch(self):
        if self.valid(): return 1

        Logger().logger.info("SunAPI REQ: %s" % self.url)
        r = requests.get(url=self.url)

        self.data = r.json()['results']
        self.cacheKey = self.getTodayAsUTC().strftime("%Y-%m-%d")

        Logger().logger.info("SunAPI: %s" % self.data)

        return 1

    def isDay(self):
        self.fetch()
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

    def getTodayAsUTC(self):
        return datetime.now(timezone.utc).astimezone(tz.tzlocal())
