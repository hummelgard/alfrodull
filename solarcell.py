#!/usr/bin/python
import os
from socketIO_client import SocketIO

#load last meassured voltage of the battery 
lastLogData = os.popen(
      "tail -n 1 /srv/http/app/htdocs/static/batterydata.txt").read().split(";")

settings = {}
with open('/srv/http/settings.txt', 'r') as file:   
    for setting in file:
        (key, val) = setting.split(":")
        settings[key] = int(val)
file.close()

batteryVoltage = float(lastLogData[5].rstrip())

if(batteryVoltage > 0 and batteryVoltage < 20):
    maxVoltage = 14.2
    startChargingVoltage = 12.40

    # turning on relay disconnects solar cell and vice verse
    charging = bool(settings['solarcell'])

    print("battery voltage:",batteryVoltage,"V","charging:",charging,"manualmode:",bool(settings['manual']))
    socketIO = SocketIO('localhost',8000)
    #If voltage above critical level, stop charging!
    if(batteryVoltage > maxVoltage and charging):

        with SocketIO('localhost', 8000,) as socketIO:
            socketIO.emit('change settings', {'data': "solarcell-latch", 'user': "server@batterymonitor", 'note':"Solcell urkopplad, batteriet 100%"})

    elif(batteryVoltage <= startChargingVoltage and not charging and settings['manual']==False):

        with SocketIO('localhost', 8000,) as socketIO:
            socketIO.emit('change settings', {'data': "solarcell-latch", 'user': "server@batterymonitor", 'note':"Solcell inkopplad"})


