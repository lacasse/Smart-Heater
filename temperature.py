#!/usr/bin/env python
import os
import time
import datetime
import logging
from rpi_rf import RFDevice

ds18b20 = ""
logging.basicConfig(filename="output.log", level=logging.INFO)


def setup():
    # Initializing temperature sensor
    global ds18b20
    for i in os.listdir("/sys/bus/w1/devices"):
        if i != "w1_bus_master1":
            ds18b20 = i

    logging.info(
        "%s **Initialized and ready**", datetime.datetime.now().strftime("%H:%M:%S")
    )
    # Reset switch
    off()
    time.sleep(1)


def read():
    # Returns the numerical temperature values
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
        output()
        if time.localtime().tm_hour == 10:
            if time.localtime().tm_min == 59:
                off()
                state = 0
            elif read() <= 24.5 and state == 0:
                on()
                state = 1
            elif read() > 24.5 and state == 1:
                off()
                state = 0

            time.sleep(9)

        else:
            time.sleep(1800)


def output():
    # Will later be used to report info to a log file and a csv to eventually graph the ambient temperature
    print(
        datetime.datetime.now().strftime("%H:%M:%S"),
        "Current temperature : %0.3f C" % read(),
    )
    logging.info(
        "%s Current temperature : %0.3f C",
        datetime.datetime.now().strftime("%H:%M:%S"),
        read(),
    )


def on():
    rfdevice = RFDevice(17)
    rfdevice.tx_repeat = 1
    rfdevice.enable_tx()
    rfdevice.tx_code(137276512, 3, 83)
    rfdevice.tx_code(17061062, 1, 190)
    rfdevice.tx_code(17061272, 3, 83)
    rfdevice.tx_code(4265267, 1, 190)
    rfdevice.cleanup()
    print(datetime.datetime.now().strftime("%H:%M:%S"), "Electric heater turned on.")
    logging.info(
        "%s Electric heater turned on.", datetime.datetime.now().strftime("%H:%M:%S")
    )


def off():
    rfdevice = RFDevice(17)
    rfdevice.tx_repeat = 1
    rfdevice.enable_tx()
    rfdevice.tx_code(4265276, 1, 188)
    rfdevice.tx_code(4265276, 1, 191)
    rfdevice.tx_code(4265276, 1, 191)
    rfdevice.tx_code(4265276, 1, 191)
    rfdevice.cleanup()
    print(datetime.datetime.now().strftime("%H:%M:%S"), "Electric heater turned off.")
    logging.info(
        "%s Electric heater turned off.", datetime.datetime.now().strftime("%H:%M:%S")
    )


def destroy():
    logging.info(
        "%s **Stopping for now**", datetime.datetime.now().strftime("%H:%M:%S")
    )
    pass


if __name__ == "__main__":
    try:
        setup()
        loop()
    except KeyboardInterrupt:
        off()
        destroy()

