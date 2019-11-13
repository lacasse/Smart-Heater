#!/usr/bin/env python
import os
import time
import datetime
from rpi_rf import RFDevice

ds18b20 = ""

def setup():
    # Reset switch
    off()
    time.sleep(1)
    global ds18b20
    for i in os.listdir("/sys/bus/w1/devices"):
        if i != "w1_bus_master1":
            ds18b20 = i


def read():
    # 	global ds18b20
    location = "/sys/bus/w1/devices/" + ds18b20 + "/w1_slave"
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    return temperature


def loop():
    state = 0
    while True:
        if time.localtime().tm_hour == 6:
            output()
            if time.localtime().tm_min == 59:
                off()
                state = 0
            elif read() <= 24 and state == 0:
                on()
                state = 1
            elif read() > 24 and state == 1:
                off()
                state = 0

            time.sleep(60)

        else:
            output()
            time.sleep(1200)


def output():
    # Will later be used to report info to a log file and a csv to eventually graph the ambient temperature
    print(datetime.datetime.now().time()," Current temperature : %0.3f C" % read())


def on():
    rfdevice = RFDevice(17)
    rfdevice.tx_repeat = 1
    rfdevice.enable_tx()
    rfdevice.tx_code(137276512, 3, 83)
    rfdevice.tx_code(17061062, 1, 190)
    rfdevice.tx_code(17061272, 3, 83)
    rfdevice.tx_code(4265267, 1, 190)
    rfdevice.cleanup()
    print(datetime.datetime.now().time()," Electric heater turned on.")


def off():
    rfdevice = RFDevice(17)
    rfdevice.tx_repeat = 1
    rfdevice.enable_tx()
    rfdevice.tx_code(8530555, 1, 190)
    rfdevice.tx_code(4265276, 1, 191)
    rfdevice.tx_code(4265276, 1, 191)
    rfdevice.cleanup()
    print(datetime.datetime.now().strftime("%H"),datetime.datetime.now().strftime("%M "),"Electric heater turned off.")


def destroy():
    pass


if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        off()
        destroy()

