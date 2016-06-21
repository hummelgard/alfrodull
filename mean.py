#!/usr/bin/python

import math, statistics

file = open('/srv/http/app/htdocs/static/weatherdata.txt', 'r')

temperature_array=[]
for line in file.readlines():

    data=line.split(';')

    if( data[0][0] != "#" ):
        row_temperature=float(data[4])
        temperature_array.append(row_temperature)
mean=statistics.mean(temperature_array)
stdev=statistics.stdev(temperature_array, mean)
print("Months mean {0:.2f} +/- {1:.2f}, \#{2}".format(mean, stdev,len(temperature_array)))

file.close()
