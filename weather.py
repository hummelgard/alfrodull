#!/usr/bin/python

from ctypes import *
import smbus, subprocess, os
import math, time
from datetime import datetime
from pytz import timezone
import pytz


BME280_REGISTER_DIG_T1       = 0x88
BME280_REGISTER_DIG_T2       = 0x8A
BME280_REGISTER_DIG_T3       = 0x8C

BME280_REGISTER_DIG_P1       = 0x8E
BME280_REGISTER_DIG_P2       = 0x90
BME280_REGISTER_DIG_P3       = 0x92
BME280_REGISTER_DIG_P4       = 0x94
BME280_REGISTER_DIG_P5       = 0x96
BME280_REGISTER_DIG_P6       = 0x98
BME280_REGISTER_DIG_P7       = 0x9A
BME280_REGISTER_DIG_P8       = 0x9C
BME280_REGISTER_DIG_P9       = 0x9E

BME280_REGISTER_DIG_H1       = 0xA1
BME280_REGISTER_DIG_H2       = 0xE1
BME280_REGISTER_DIG_H3       = 0xE3
BME280_REGISTER_DIG_H4       = 0xE4
BME280_REGISTER_DIG_H5       = 0xE5
BME280_REGISTER_DIG_H6       = 0xE7
 
BME280_REGISTER_CHIPID       = 0xD0
BME280_REGISTER_VERSION      = 0xD1
BME280_REGISTER_SOFTRESET    = 0xE0

BME280_REGISTER_CAL26        = 0xE1  # R calibration stored in 0xE1-0xF0

BME280_REGISTER_CONTROLHUMID = 0xF2
BME280_REGISTER_CONTROL      = 0xF4
BME280_REGISTER_CONFIG       = 0xF5
BME280_REGISTER_PRESSUREDATA = 0xF7
BME280_REGISTER_TEMPDATA     = 0xFA
BME280_REGISTER_HUMIDDATA    = 0xFD

BME280_ADDRESS               = 0x77


class Adafruit_I2C :

  def __init__(self, address, busnum=-1, debug=False):
    self.address = address
    self.bus = smbus.SMBus(busnum if busnum >= 0 else 1)
    self.debug = debug

  def reverseByteOrder(self, data):
    "Reverses the byte order of an int (16-bit) or long (32-bit) value"
    # Courtesy Vishal Sapre
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
      val    = (val << 8) | (data & 0xff)
      data >>= 8
    return val

  def errMsg(self):
    print("Error accessing 0x%02X: Check your I2C address" % self.address)
    return -1

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    try:
      #time.sleep(3)
      self.bus.write_byte_data(self.address, reg, value)
      if self.debug:
        print("I2C: Wrote 0x%02X to register 0x%02X" % (value, reg))
    except IOError as err:
      return self.errMsg()

  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    try:
      #time.sleep(3)
      result = self.bus.read_byte_data(self.address, reg)
      if self.debug:
        print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except IOError as err:
      return self.errMsg()

  def readS8(self, reg):
    "Reads a signed byte from the I2C device"
    try:
      #time.sleep(3)
      result = self.bus.read_byte_data(self.address, reg)
      if result > 127: result -= 256
      if self.debug:
        print("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except IOError as err:
      return self.errMsg()

  def readU16(self, reg):
    "Reads an unsigned 16-bit value from the I2C device"
    try:
      #time.sleep(3)
      result = self.bus.read_word_data(self.address,reg)
      if (self.debug):
        print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
      return result
    except IOError as err:
      return self.errMsg()

  def readS16(self, reg):
    "Reads a signed 16-bit value from the I2C device"
    try:
      #time.sleep(3)
      result = self.bus.read_word_data(self.address,reg)
      if result > 32767: result -= 65536
      if (self.debug):
        print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
      return result
    except IOError as err:
      return self.errMsg()




#---------------------------------------------------------------------------------


bme280 = Adafruit_I2C(0x77)

while True:
    dig_T1 = bme280.readU16(BME280_REGISTER_DIG_T1)
    dig_T2 = bme280.readS16(BME280_REGISTER_DIG_T2)
    dig_T3 = bme280.readS16(BME280_REGISTER_DIG_T3)

    dig_P1 = bme280.readU16(BME280_REGISTER_DIG_P1)
    dig_P2 = bme280.readS16(BME280_REGISTER_DIG_P2)
    dig_P3 = bme280.readS16(BME280_REGISTER_DIG_P3)
    dig_P4 = bme280.readS16(BME280_REGISTER_DIG_P4)
    dig_P5 = bme280.readS16(BME280_REGISTER_DIG_P5)
    dig_P6 = bme280.readS16(BME280_REGISTER_DIG_P6)
    dig_P7 = bme280.readS16(BME280_REGISTER_DIG_P7)
    dig_P8 = bme280.readS16(BME280_REGISTER_DIG_P8)
    dig_P9 = bme280.readS16(BME280_REGISTER_DIG_P9)

    dig_H1 = bme280.readU8(BME280_REGISTER_DIG_H1)
    dig_H2 = bme280.readS16(BME280_REGISTER_DIG_H2)
    dig_H3 = bme280.readU8(BME280_REGISTER_DIG_H3)
    dig_H4 = (bme280.readU8(BME280_REGISTER_DIG_H4) << 4) | (bme280.readU8(BME280_REGISTER_DIG_H4+1) & 0xF);
    dig_H5 = (bme280.readU8(BME280_REGISTER_DIG_H5+1) << 4) | (bme280.readU8(BME280_REGISTER_DIG_H5) >> 4);
    dig_H6 = bme280.readU8(BME280_REGISTER_DIG_H6)

    # max resoultion, lowest sample speed
    #bme280.write8(BME280_REGISTER_CONTROLHUMID, 0b101 )
    #bme280.write8(BME280_REGISTER_CONTROL, 0b010110101 )

    # change oversampling for humidity in above line from x16 to x1
    bme280.write8(BME280_REGISTER_CONTROLHUMID, 0b001 )
    bme280.write8(BME280_REGISTER_CONTROL, 0b00100101 )
    # the last two bits, controls sleep mode=00, forced=01 or 10, normal=11

    # min resolution, fastest sample speed
    #bme280.write8(BME280_REGISTER_CONTROLHUMID, 0b00000001 )
    #bme280.write8(BME280_REGISTER_CONTROL, 0b00100111 )


    #READ TEMPERATURE
    adc_T = bme280.reverseByteOrder(bme280.readU16(BME280_REGISTER_TEMPDATA))
    adc_T <<= 8
    adc_T |= bme280.readU8(BME280_REGISTER_TEMPDATA+2)
    adc_T >>= 4

    var1  = ( (adc_T >>3) - (dig_T1 <<1) )  * dig_T2 >> 11

    var2  = ((((((adc_T>>4) - (int(dig_T1))) * ((adc_T>>4) - (int(dig_T1)))) >> 12) * (int(dig_T3))) >> 14)

    t_fine = var1 + var2

    temperature = ((t_fine * 5 + 128) >> 8)/100.0

    #print("Temp: {0:15.2f}".format(temperature))


    #READ PRESSURE
    adc_P = bme280.reverseByteOrder(bme280.readU16(BME280_REGISTER_PRESSUREDATA))
    adc_P <<= 8

    adc_P |= bme280.readU8(BME280_REGISTER_PRESSUREDATA+2)
    adc_P >>= 4

    var1 = t_fine - 128000
    var2 = var1 * var1 * dig_P6
    var2 = var2 + ((var1*dig_P5)<<17)
    var2 = var2 + ((dig_P4)<<35)
    var1 = ( ((var1 * var1 * dig_P3)>>8) + 
             ((var1 * dig_P2)<<12) )

    var1 = ((((1)<<47)+var1))*(dig_P1)>>33

    p = 1048576 - adc_P
    p = (((p<<31) - var2)*3125) // var1
    var1 = (int(dig_P9) * (p>>13) * (p>>13) ) >> 25
    var2 = (int(dig_P8) * p) >> 19

    p = ((p + var1 + var2) >> 8) + ((dig_P7)<<4)
    pressure = p/256

    #print("Pres: {0:15.2f}".format(pressure))


    #READ HUMIDITY
    adc_H = bme280.reverseByteOrder(bme280.readU16(BME280_REGISTER_HUMIDDATA))

    v_x1_u32r = (t_fine - 76800)

    v_x1_u32r = (((((adc_H << 14) - (dig_H4 << 20) -
                (dig_H5 * v_x1_u32r)) + 16384) >> 15) *
                   (((((((v_x1_u32r * dig_H6) >> 10) *
                  (((v_x1_u32r * dig_H3) >> 11) + 32768)) >> 10) +
                2097152) * dig_H2 + 8192) >> 14))

    v_x1_u32r = (v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) *
                    dig_H1) >> 4))


    if (v_x1_u32r < 0): 
        v_x1_u32r = 0

    if (v_x1_u32r > 419430400): 
        v_x1_u32r = 419430400


    humidity = (v_x1_u32r>>12)/1024.0

    #print("Humi: {0:15.2f}".format(humidity))
    if(humidity<101 and humidity>0 and 
       pressure>95000 and pressure<105000 and 
       temperature<50 and temperature>-50):
       break
    else:
       f = open('/srv/http/app/htdocs/static/errors-weather.txt', 'a')
       locale_date = timezone("Europe/Stockholm").localize(datetime.now())
       utc_date = locale_date.astimezone(timezone("utc"))
       fmt = '%Y-%m-%d_%H:%M:%S;%Z%z'

       f.write(utc_date.strftime(fmt) + ";" +
               locale_date.strftime(fmt) +
               ";{0:.2f};{1:.2f};{2:.2f}\n".format(temperature, humidity, pressure) )
       f.close()
       time.sleep(20)

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

lastLogData = os.popen("tail -n 1 /srv/http/app/htdocs/static/weatherdata.txt").read().split(";")
if( float(lastLogData[5]) == 100 and humidity == 100):
    humidity = 99.9


f = open('/srv/http/app/htdocs/static/weatherdata.txt', 'a')

locale_date = timezone("Europe/Stockholm").localize(datetime.now())
utc_date = locale_date.astimezone(timezone("utc"))

fmt = '%Y-%m-%d_%H:%M:%S;%Z%z'

f.write(utc_date.strftime(fmt) + ";" +
        locale_date.strftime(fmt) +
        ";{0:.2f};{1:.2f};{2:.2f};{3:.2f}\n".format(temperature, humidity, pressure, dewpoint) )
f.close()

plot=True
if( plot==True ):
    plot = subprocess.Popen(['gnuplot','/srv/http/weather.gnuplot'], stdin=subprocess.PIPE)

    plot.stdin.flush()
    plot.wait()



