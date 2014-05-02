# -*- coding: utf-8 -*-
from yr.libyr import Yr

weather = Yr('Norge/Akershus/Bærum/Halden_brygge')
now_json = weather.wind_speed()
print(now_json)
