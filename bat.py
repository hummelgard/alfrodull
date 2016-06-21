#!/usr/bin/python

from ctypes import *
import smbus, subprocess, os
import math, time
from datetime import datetime
from pytz import timezone
import pytz

INA219_ADDRESS                          = 0x40
INA219_READ                             = 0x01


INA219_REG_CONFIG                       = 0x00

INA219_CONFIG_RESET                     = 0x8000
	
INA219_CONFIG_BVOLTAGERANGE_MASK        = 0x2000
INA219_CONFIG_BVOLTAGERANGE_16V         = 0x0000
INA219_CONFIG_BVOLTAGERANGE_32V         = 0x2000
	
INA219_CONFIG_GAIN_MASK                 = 0x1800
INA219_CONFIG_GAIN_1_40MV               = 0x0000
INA219_CONFIG_GAIN_2_80MV               = 0x0800
INA219_CONFIG_GAIN_4_160MV              = 0x1000
INA219_CONFIG_GAIN_8_320MV              = 0x1800
	
INA219_CONFIG_BADCRES_MASK              = 0x0780
INA219_CONFIG_BADCRES_9BIT              = 0x0080
INA219_CONFIG_BADCRES_10BIT             = 0x0100
INA219_CONFIG_BADCRES_11BIT             = 0x0200
INA219_CONFIG_BADCRES_12BIT             = 0x0400
    
INA219_CONFIG_SADCRES_MASK              = 0x0078
INA219_CONFIG_SADCRES_9BIT_1S_84US      = 0x0000
INA219_CONFIG_SADCRES_10BIT_1S_148US    = 0x0008
INA219_CONFIG_SADCRES_11BIT_1S_276US    = 0x0010
INA219_CONFIG_SADCRES_12BIT_1S_532US    = 0x0018
INA219_CONFIG_SADCRES_12BIT_2S_1060US   = 0x0048
INA219_CONFIG_SADCRES_12BIT_4S_2130US   = 0x0050
INA219_CONFIG_SADCRES_12BIT_8S_4260US   = 0x0058
INA219_CONFIG_SADCRES_12BIT_16S_8510US  = 0x0060
INA219_CONFIG_SADCRES_12BIT_32S_17MS    = 0x0068
INA219_CONFIG_SADCRES_12BIT_64S_34MS    = 0x0070
INA219_CONFIG_SADCRES_12BIT_128S_69MS   = 0x0078
	
INA219_CONFIG_MODE_MASK                 = 0x0007
INA219_CONFIG_MODE_POWERDOWN            = 0x0000
INA219_CONFIG_MODE_SVOLT_TRIGGERED      = 0x0001
INA219_CONFIG_MODE_BVOLT_TRIGGERED      = 0x0002
INA219_CONFIG_MODE_SANDBVOLT_TRIGGERED  = 0x0003
INA219_CONFIG_MODE_ADCOFF               = 0x0004
INA219_CONFIG_MODE_SVOLT_CONTINUOUS     = 0x0005
INA219_CONFIG_MODE_BVOLT_CONTINUOUS     = 0x0006
INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS = 0x0007	

INA219_REG_SHUNTVOLTAGE                 = 0x01
INA219_REG_BUSVOLTAGE                   = 0x02
INA219_REG_POWER                        = 0x03
INA219_REG_CURRENT                      = 0x04
INA219_REG_CALIBRATION                  = 0x05

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

  def write16(self, reg, value):
    "Writes a 16-bit value to the specified register/address pair"
    try:
      self.bus.write_word_data(self.address, reg, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X" %
         (value, reg, reg+1))
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
        print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % 
          (self.address, result & 0xFFFF, reg))
      return result
    except IOError as err:
      return self.errMsg()

  def readS16(self, reg):
    "Reads a signed 16-bit value from the I2C device"
    try:
      #time.sleep(3)
      data = self.bus.read_word_data(self.address,reg)
      data = data & 0xFFFF

      print(ina219.reverseByteOrder(data))
      byteCount = len(hex(data)[2:].replace('L','')[::2])
      val       = 0
      for i in range(byteCount):
        val    = (val << 8) | (data & 0xff)
        data >>= 8
      
      result = val

      if result > 32767: result -= 65536

      if (self.debug):
        print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % 
          (self.address, result, reg))
      return result
    except IOError as err:
      return self.errMsg()




#------------------------------------------------------------------------------


ina219 = Adafruit_I2C(INA219_ADDRESS)

while True:

    # parameters for 1.6A range
    #ina219_calValue = 10240 # 1A
    #ina219_currentDivider_mA = 25
    
    # parameters for 3.2A range
    ina219_calValue = 4096 # 2A
    ina219_currentDivider_mA = 10

    ina219.write16(INA219_REG_CALIBRATION, 
                   ina219.reverseByteOrder(ina219_calValue))

    config = (INA219_CONFIG_BVOLTAGERANGE_16V |
         INA219_CONFIG_GAIN_8_320MV |
         INA219_CONFIG_BADCRES_12BIT |
         INA219_CONFIG_SADCRES_12BIT_128S_69MS |
         INA219_CONFIG_MODE_SANDBVOLT_CONTINUOUS)

    ina219.write16(INA219_REG_CONFIG, ina219.reverseByteOrder(config))
    
    shuntvoltage = ina219.reverseByteOrder(ina219.readU16(
                                           INA219_REG_SHUNTVOLTAGE)) * 0.01  

    shuntcurrentList = [] 
    busvoltageList = [] 
    samples = 5
    for i in range(samples):
        busvoltageList.append( (ina219.readS16(INA219_REG_BUSVOLTAGE) >> 3) * 4 * 0.001)     
        shuntcurrentList.append( ina219.readS16(INA219_REG_CURRENT) )

    busvoltage = sorted(busvoltageList)[samples//2]
    shuntcurrentRAW =sorted(shuntcurrentList)[samples//2]
    shuntcurrent = sorted(shuntcurrentList)[samples//2] / ina219_currentDivider_mA 

    print("busvoltage",busvoltage,"V")
    print("shuntvoltage",shuntvoltage,"mV")
    print("shuntcurrentRAW",shuntcurrentRAW)
    print("shuntcurrent",shuntcurrent,"mA")

    if(shuntcurrent<5000 and shuntcurrent>-5000 and 
       busvoltage>1 and busvoltage<100):
       break
    else:
       f = open('/srv/http/app/htdocs/static/errors-battery.txt', 'a')
       locale_date = timezone("Europe/Stockholm").localize(datetime.now())
       utc_date = locale_date.astimezone(timezone("utc"))
       fmt = '%Y-%m-%d_%H:%M:%S;%Z%z'

       f.write(utc_date.strftime(fmt) + ";" +
               locale_date.strftime(fmt) +
               ";{0:+.1f};{1:+.1f};{2:.3f}\n".format(shuntcurrent, 
                                                     shuntvoltage, busvoltage))
       f.close()
       time.sleep(5)

batterycurrent = shuntcurrent
batteryvoltage = busvoltage
#------------------------------------------------------------------------------



lastLogData = os.popen(
      "tail -n 1 /srv/http/app/htdocs/static/batterydata.txt").read().split(";")


f = open('/srv/http/app/htdocs/static/batterydata.txt', 'a')

locale_date = timezone("Europe/Stockholm").localize(datetime.now())
utc_date = locale_date.astimezone(timezone("utc"))

fmt = '%Y-%m-%d_%H:%M:%S;%Z%z'

#f.write(utc_date.strftime(fmt) + ";" +
#        locale_date.strftime(fmt) +
#        ";{0:+.1f};{1:.3f}\n".format(batterycurrent, batteryvoltage) )
#f.close()

plot=False
if( plot==True ):
    plot = subprocess.Popen(['gnuplot','battery.gnuplot'], stdin=subprocess.PIPE)

    plot.stdin.flush()
    plot.wait()



