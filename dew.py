import math
f1 = open('/srv/http/app/htdocs/static/weatherdata.txt.old', 'r')
f2 = open('/srv/http/app/htdocs/static/weatherdata.txt', 'w')


for line in f1.readlines():
    data=line.split(";")
   
    locale_date = data[2] + ";" + data[3]
    utc_date = data[0] + ";"+ data[1]
    temperature = float(data[4])
    humidity =float(data[5])
    pressure = float(data[6])
    if(data[0][0]!='#'):
      print(temperature,humidity,pressure)
      # DEW POINT CALCULATION
      #(1) Saturation Vapor Pressure = ESGG(T)
      RATIO = 373.15 / (273.15 + temperature)
      RHS = -7.90298 * (RATIO - 1)
      RHS += 5.02808 * math.log10(RATIO)
      RHS += -1.3816e-7 * (math.pow(10, (11.344 * (1 - 1/RATIO ))) - 1)
      RHS += 8.1328e-3 * (math.pow(10, (-3.49149 * (RATIO - 1))) - 1)
      RHS += math.log10(1013.246)

      #(2) DEWPOINT = F(Vapor Pressure)
      VP = math.pow(10, RHS - 3) * humidity
      T = math.log(VP/0.61078)
      dewpoint = (241.88 * T) / (17.558 - T)



    #locale_date = timezone("Europe/Stockholm").localize(datetime.now())
    #utc_date = locale_date.astimezone(timezone("utc"))

    #fmt = '%Y-%m-%d_%H:%M:%S;%Z%z'

      f2.write(utc_date + ";" +
        locale_date +
        ";{0:.2f};{1:.2f};{2:.2f};{3:.2f}\n".format(temperature, humidity, pressure, dewpoint) )
f1.close()
f2.close()
