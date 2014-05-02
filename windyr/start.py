# -*- coding: utf-8 -*-
from yr.libyr import Yr
from email.mime.text import MIMEText
from datetime import datetime
from dateutil.parser import parse
import smtplib
from getpass import getpass


class WindLocator(object):
    WORK_DAY = range(0, 5)  # Mon - Fri
    WEEKEND = range(6, 8)  # Sat, Sun
    location = 'Norge/Akershus/Bærum/Halden_brygge'
    time_limits = {WORK_DAY: 16, WEEKEND: 8}
    wind_limit = 5.0  # m/s
    username = input('Email address:')
    password = getpass()

    def __init__(self):
        self.weather_api = Yr(self.location)

    def get_interesting_hour(self):
        '''
        This method tells us at after what hour in the day
        we are interested in getting wind data
        '''
        day_of_week = datetime.today().weekday()
        for weekdays, time in self.time_limits.items():
            if day_of_week in weekdays:
                return time

    def sort_time_data(self, intervals):
        '''
        Sort by time of day, but only show today's date
        '''
        from datetime import timedelta
        interesting_day = datetime.today().date() + timedelta(days=1)
        for interval in intervals:
            date = parse(interval['from']).date()
            if date == interesting_day:
                yield interval

    def run(self):
        print('[~] Getting weather data')
        now_json = self.weather_api.wind_speed()['data']
        print('[~] Got weather data')
        limit = self.get_interesting_hour()
        intervals = self.sort_time_data(now_json)
        for time_interval in intervals:
            if parse(time_interval['from']).time().hour < limit:
                continue
            if time_interval['speed'] > self.wind_limit:
                self.send_message(time_interval)
                return

    def send_message(self, interval):
        msg = MIMEText('Wind alert: %s\nFrom %s to %s\nWindspeed: %s'
                       % (self.location, interval['from'], interval['to'],
                          interval['speed']))
        msg['Subject'] = ('Wind looks good: (%s) %s at %s'
                          % (self.location, interval['speed'],
                             interval['from']))
        msg['From'] = self.username
        msg['To'] = self.username

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.username, self.password)
        server.send_message(msg)
        server.close()
        print('[~] Sent Message')

if __name__ == '__main__':
    locator = WindLocator()
    locator.run()
