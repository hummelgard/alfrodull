#!/bin/bash

# configures pin17 on the gpio port to suit connected relay.
echo "17" > /sys/class/gpio/export
echo "out" > /sys/class/gpio/gpio17/direction
echo "0" > /sys/class/gpio/gpio17/value
chown http:http /sys/class/gpio/gpio17/value

