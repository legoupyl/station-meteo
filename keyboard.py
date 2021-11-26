# Adafruit Raspberry Pi MPR121 Keyboard Example
# Author: Tony DiCola
#
# Allows you to turn touches detected by the MPR121 into key presses on a
# Raspberry Pi.
#
# NOTE: This only works with a Raspberry Pi right now because it depends on some
# specific event detection logic in the RPi.GPIO library.
#
# Dependencies
# ============
#
# Make sure you have the required dependencies by executing the following commands:
#   sudo apt-get update
#   sudo apt-get install build-essential python-dev python-pip libudev-dev
#   sudo pip install python-uinput
#
# Also make sure you have installed the Adafruit Python MPR121 library by running
# its setup.py (in the parent directory):
#   sudo python setup.py install
#
# Usage
# =====
#
# To use this program you first need to connect the MPR121 board to the Raspberry
# Pi (either connect the HAT directly to the Pi, or wire the I2C pins SCL, SDA to
# the Pi SCL, SDA, VIN to Pi 3.3V, GND to Pi GND).  If you aren't using the HAT
# version of the board you must connect the IRQ pin to a free digital input on the
# Pi (the default is 26).
#
# Next define the mapping of capacitive touch input presses to keyboard
# button presses.  Scroll down to the KEY_MAPPING dictionary definition below
# and adjust the configuration as described in its comments.
#
# If you're using a differnet pin for the IRQ line change the IRQ_PIN variable
# below to the pin number you're using.  Don't change this if you're using the
# HAT version of the board as it's built to use pin 26 as the IRQ input.
#
# Finally run the script as root:
#   sudo python keyboard.py
#
# Try pressing buttons and you should see key presses made on the Pi!
#
# Press Ctrl-C to quit at any time.
#
# Copyright (c) 2014 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import atexit
import logging
import subprocess
import sys
import time

import Adafruit_MPR121.MPR121 as MPR121
import RPi.GPIO as GPIO

# Input pin connected to the capacitive touch sensor's IRQ output.
# For the capacitive touch HAT this should be pin 26!
IRQ_PIN = 13

# Don't change the below values unless you know what you're doing.  These help
# adjust the load on the CPU vs. responsiveness of the key detection.
MAX_EVENT_WAIT_SECONDS = 0.5
EVENT_WAIT_SLEEP_SECONDS = 0.1


# Uncomment to enable debug message logging (might slow down key detection).
#logging.basicConfig(level=logging.DEBUG)

# Make sure uinput kernel module is loaded.
#subprocess.check_call(['modprobe', 'uinput'])

# Configure virtual keyboard.
#device = uinput.Device(KEY_MAPPING.values())

# Setup the MPR121 device.
cap = MPR121.MPR121()
if not cap.begin():
    print('Failed to initialize MPR121, check your wiring!')
    sys.exit(1)

def inter1(pin):
	touched = cap.touched()
	print (touched)

# Configure GPIO library to listen on IRQ pin for changes.
# Be sure to configure pin with a pull-up because it is open collector when not
# enabled.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IRQ_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(IRQ_PIN, GPIO.FALLING, inter1)
atexit.register(GPIO.cleanup)

# Clear any pending interrupts by reading touch state.
cap.touched()

# Event loop to wait for IRQ pin changes and respond to them.
print('Press Ctrl-C to quit.')
while True:
    # Wait for the IRQ pin to drop or too much time ellapses (to help prevent
    # missing an IRQ event and waiting forever).
    start = time.time()
    #while (time.time() - start) < MAX_EVENT_WAIT_SECONDS and not GPIO.event_detected(IRQ_PIN):
     #   time.sleep(EVENT_WAIT_SLEEP_SECONDS)
    # Read touch state.
