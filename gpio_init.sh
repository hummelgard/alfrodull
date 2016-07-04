#!/bin/bash

# configures pin17 on the gpio port to suit connected relay.
echo "17" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio17/direction
echo "0" > /sys/class/gpio/gpio17/value
chown http:http /sys/class/gpio/gpio17/value


# configures pin22 on the gpio port to suit connected relay.
echo "22" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio22/direction
echo "0" > /sys/class/gpio/gpio22/value
chown http:http /sys/class/gpio/gpio22/value


# configures pin27 on the gpio port to suit connected relay.
echo "27" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio27/direction
echo "0" > /sys/class/gpio/gpio27/value
chown http:http /sys/class/gpio/gpio27/value



