#!/usr/bin/python

DATA_FROM_YR = True

from datetime import datetime
from datetime import timedelta
import json, locale, time
from yr.libyr import Yr

#licens text, ges som som länk till aktuell vädersida
#Vêrvarsel frå Yr levert av Meteorologisk institutt og NRK


#http://www.yr.no/place/Sweden/V%C3%A4sternorrland/Ortsj%C3%B6n/forecast.xml

if DATA_FROM_YR:
    weather = Yr(location_name='Sweden/V%C3%A4sternorrland/Ortsj%C3%B6n')


    filestr = "["
    for forecast in weather.forecast(as_json=True):
        filestr += forecast + ","

    filestr = filestr[:-1]
    filestr += "]"
    
    file = open('/srv/http/yr-prognos.txt', 'w')
    file.write(filestr)  
    file.close()
    forecast = filestr
    
else:
    file = open('/srv/http/yr-prognos.txt', 'r')    
    forecast = file.read()
    file.close()


forecast_json = json.loads(forecast)



locale.setlocale(locale.LC_ALL,"sv_SE.utf8")

day = timedelta(days=1)
#mon_str = "måndag".encode('ascii', 'xmlcharrefreplace').decode('utf8')
#tis_str = "tisdag".encode('ascii', 'xmlcharrefreplace').decode('utf8')
#today_str = time.strftime("%A").encode('ascii', 'xmlcharrefreplace').decode('utf8')

now = datetime.now()
day_str = [(now + 1 * day).strftime("%A").encode('ascii', 'xmlcharrefreplace').decode('utf8'),
           (now + 2 * day).strftime("%A").encode('ascii', 'xmlcharrefreplace').decode('utf8'),
           (now + 3 * day).strftime("%A").encode('ascii', 'xmlcharrefreplace').decode('utf8'),
           (now + 4 * day).strftime("%A").encode('ascii', 'xmlcharrefreplace').decode('utf8'),
           (now + 5 * day).strftime("%A").encode('ascii', 'xmlcharrefreplace').decode('utf8')]


day = 0

sunlight = 0
filestr_sun = ""
filestr_weather = ""
for dayforecast in forecast_json:
    if( dayforecast['@from'].split('T')[0] != now.strftime("%Y-%m-%d") ):

        # sum only day events, skipping night time
        if dayforecast['@period'] is "1" or dayforecast['@period'] is "2":
            val = int(dayforecast['symbol']['@number'])
            # soligt väder
            if(val == 1): weight = 1 # 
            elif(val == 2): weight = 2 # 
            elif(val == 3): weight = 3

            # lätta byar
            elif(val == 40): weight = 4 # regn
            elif(val == 24): weight = 4 # regn med åska
            elif(val == 42): weight = 4 # snöblandat
            elif(val == 26): weight = 4 # snöblandat med åska
            elif(val == 44): weight = 4 # snö
            elif(val == 28): weight = 4 # snö med åska

            # byar
            elif(val == 5): weight = 5 # regn 
            elif(val == 6): weight = 5 # regn med åska
            elif(val == 7): weight = 5 # snöblandat
            elif(val == 20): weight = 5 # snöblandat med åska
            elif(val == 8): weight = 5 # snö
            elif(val == 21): weight = 5 # snö med åska
            
            # kraftiga byar
            elif(val == 25): weight = 6 # regn med åska
            elif(val == 43): weight = 6 # snöbladnat
            elif(val == 27): weight = 6 # snöblandat med åska
            elif(val == 45): weight = 6 # snö
            elif(val == 29): weight = 6 # snö med åska

            # moln
            elif(val == 4): weight = 7 # regn
  
            # lätt nederbörd
            elif(val == 46): weight = 8 # regn
            elif(val == 30): weight = 8 # regn med åska
            elif(val == 47): weight = 8 # snöblandat 
            elif(val == 31): weight = 8 # snöblandat med åska 
            elif(val == 49): weight = 8 # snö 
            elif(val == 33): weight = 8 # snö med åska 
          
            # nederbörd
            elif(val == 9): weight = 9 # regn
            elif(val == 22): weight = 9 # regn med åska
            elif(val == 12): weight = 9 # snöblandat 
            elif(val == 23): weight = 9 # snöblandat med åska 
            elif(val == 13): weight = 9 # snö 
            elif(val == 14): weight = 9 # snö med åska 
      
            # kraftigt nederbörd
            elif(val == 10): weight = 10 # regn
            elif(val == 11): weight = 10 # regn med åska
            elif(val == 48): weight = 10 # snöblandat 
            elif(val == 32): weight = 10 # snöblandat med åska
            elif(val == 50): weight = 10 # snö
            elif(val == 34): weight = 10 # snö med åska
    
            # dimma
            elif(val == 15): weight = 11 # dimma
            
            else: weight = 99 # error, correlates to no symbol

            sunlight += weight


        if dayforecast['@period'] is "2":

            filestr_sun = filestr_sun + ("{0}:{1}\n".format(day_str[day],sunlight))
            filestr_weather = filestr_weather + ( "{0}:{1}\n".format(day_str[day],
                                                  dayforecast['symbol']['@var']) )
            sunlight = 0
            day = day + 1
        if day is 5:
            break

file = open('/srv/http/solprognosdata.txt', 'w')
file.write(filestr_sun)  
file.close()

file = open('/srv/http/prognosdata.txt', 'w')
file.write(filestr_weather)  
file.close()










