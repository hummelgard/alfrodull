#!/usr/bin/python

from ctypes import *
import smbus, subprocess, os
import math, time
from datetime import datetime
from pytz import timezone
import pytz

TSL2591_ADDRESS                     = 0x29

TSL2591_VISIBLE                     = 2 
TSL2591_INFRARED                    = 1
TSL2591_FULLSPECTRUM                = 0

TSL2591_ADDR                        = 0x29
TSL2591_READBIT                     = 0x01

TSL2591_COMMAND_BIT                 = 0xA0
TSL2591_CLEAR_INT                   = 0xE7
TSL2591_TEST_INT                    = 0xE4
TSL2591_WORD_BIT                    = 0x20
TSL2591_BLOCK_BIT                   = 0x10

TSL2591_ENABLE_POWEROFF             = 0x00
TSL2591_ENABLE_POWERON              = 0x01
TSL2591_ENABLE_AEN                  = 0x02
TSL2591_ENABLE_AIEN                 = 0x10
TSL2591_ENABLE_NPIEN                = 0x80

TSL2591_LUX_DF                      = 408.0
TSL2591_LUX_COEFB                   = 1.64
TSL2591_LUX_COEFC                   = 0.59
TSL2591_LUX_COEFD                   = 0.86

TSL2591_REGISTER_ENABLE             = 0x00
TSL2591_REGISTER_CONTROL            = 0x01
TSL2591_REGISTER_THRESHOLD_AILTL    = 0x04
TSL2591_REGISTER_THRESHOLD_AILTH    = 0x05
TSL2591_REGISTER_THRESHOLD_AIHTL    = 0x06
TSL2591_REGISTER_THRESHOLD_AIHTH    = 0x07
TSL2591_REGISTER_THRESHOLD_NPAILTL  = 0x08
TSL2591_REGISTER_THRESHOLD_NPAILTH  = 0x09
TSL2591_REGISTER_THRESHOLD_NPAIHTL  = 0x0A
TSL2591_REGISTER_THRESHOLD_NPAIHTH  = 0x0B
TSL2591_REGISTER_PERSIST_FILTER     = 0x0C
TSL2591_REGISTER_PACKAGE_PID        = 0x11
TSL2591_REGISTER_DEVICE_ID          = 0x12
TSL2591_REGISTER_DEVICE_STATUS      = 0x13
TSL2591_REGISTER_CHAN0_LOW          = 0x14
TSL2591_REGISTER_CHAN0_HIGH         = 0x15
TSL2591_REGISTER_CHAN1_LOW          = 0x16
TSL2591_REGISTER_CHAN1_HIGH         = 0x17

TSL2591_INTEGRATIONTIME_100MS       = 0x00
TSL2591_INTEGRATIONTIME_200MS       = 0x01
TSL2591_INTEGRATIONTIME_300MS       = 0x02
TSL2591_INTEGRATIONTIME_400MS       = 0x03
TSL2591_INTEGRATIONTIME_500MS       = 0x04
TSL2591_INTEGRATIONTIME_600MS       = 0x05

TSL2591_PERSIST_EVERY               = 0x00
TSL2591_PERSIST_ANY                 = 0x01
TSL2591_PERSIST_2                   = 0x02
TSL2591_PERSIST_3                   = 0x03
TSL2591_PERSIST_5                   = 0x04
TSL2591_PERSIST_10                  = 0x05
TSL2591_PERSIST_15                  = 0x06
TSL2591_PERSIST_20                  = 0x07
TSL2591_PERSIST_25                  = 0x08
TSL2591_PERSIST_30                  = 0x09
TSL2591_PERSIST_35                  = 0x0A
TSL2591_PERSIST_40                  = 0x0B
TSL2591_PERSIST_45                  = 0x0C
TSL2591_PERSIST_50                  = 0x0D
TSL2591_PERSIST_55                  = 0x0E
TSL2591_PERSIST_60                  = 0x0F

TSL2591_GAIN_LOW                    = 0x00
TSL2591_GAIN_MED                    = 0x10
TSL2591_GAIN_HIGH                   = 0x20
TSL2591_GAIN_MAX                    = 0x30

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
      result = self.bus.read_word_data(self.address,reg)
      if result > 32767: result -= 65536
      if (self.debug):
        print("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % 
          (self.address, result & 0xFFFF, reg))
      return result
    except IOError as err:
      return self.errMsg()


#------------------------------------------------------------------------------


TSL2591 = Adafruit_I2C(TSL2591_ADDRESS)



#TSL2591.readS8(TSL2591_COMMAND_BIT | TSL2591_REGISTER_DEVICE_ID)

TSL2591.write8(TSL2591_COMMAND_BIT | TSL2591_REGISTER_ENABLE, TSL2591_ENABLE_POWERON | TSL2591_ENABLE_AEN | TSL2591_ENABLE_AIEN | TSL2591_ENABLE_NPIEN)

# set these bits 0xb00000aaa to following:
# 000 for 100ms
# 001 200ms
# 010 300ms
# 011 400ms
# 100 500ms
# 101 600ms

integration = 0b00000101 # 100,200,...,600

# set these bits 0xb00aa0000 to following:
# 00 low gain
# 01 medium
# 10 high
# 11 max gain
gain = 0b00000000 #bit 4,5 #1 # 1,25,428,9876


TSL2591.write8(TSL2591_COMMAND_BIT | TSL2591_REGISTER_CONTROL, integration | gain)

# read one dump value to settle the sensor
TSL2591.readU16(TSL2591_COMMAND_BIT | TSL2591_REGISTER_CHAN1_LOW)
TSL2591.readU16(TSL2591_COMMAND_BIT | TSL2591_REGISTER_CHAN0_LOW)

x = TSL2591.readU16(TSL2591_COMMAND_BIT | TSL2591_REGISTER_CHAN1_LOW)
x <<= 16
x |=TSL2591.readU16(TSL2591_COMMAND_BIT | TSL2591_REGISTER_CHAN0_LOW)

full =  (x & 0xFFFF)
ir = (x >> 16)
vis = ( (x & 0xFFFF) - (x >> 16))
#print(x, full, ir, vis)

atime = 600
again = 1
ch0 = full
ch1 = ir
cpl = (atime * again) / TSL2591_LUX_DF

lux1 = ( ch0 - (TSL2591_LUX_COEFB * ch1) ) / cpl
lux2 = ( ( TSL2591_LUX_COEFC * ch0 ) - ( TSL2591_LUX_COEFD * ch1 ) ) / cpl

if(lux1>lux2):
  lux = lux1
else:
  lux = lux2

#print(lux)

# second alternative method  lux = ch0 - ( 1.7 * ch1 ) ) / cpl

#------------------------------------------------------------------------------



lastLogData = os.popen("tail -n 1 /srv/http/app/htdocs/static/sunlightdata.txt").read().split(";")


f = open('/srv/http/app/htdocs/static/sunlightdata.txt', 'a')

locale_date = timezone("Europe/Stockholm").localize(datetime.now())
utc_date = locale_date.astimezone(timezone("utc"))

fmt = '%Y-%m-%d_%H:%M:%S;%Z%z'

f.write(utc_date.strftime(fmt) + ";" +
        locale_date.strftime(fmt) +
        ";{0:.2f};{1:.0f};{2:.0f}\n".format(lux, ch0, ch1) )
f.close()

plot=True
if( plot==True ):
    plot = subprocess.Popen(['gnuplot','/srv/http/sunlight.gnuplot'], stdin=subprocess.PIPE)

    plot.stdin.flush()
    plot.wait()

