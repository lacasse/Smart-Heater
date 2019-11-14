#!/usr/bin/env python3
from rpi_rf import RFDevice

rfdevice = RFDevice(17)
rfdevice.enable_tx()
rfdevice.tx_repeat = 1

rfdevice.tx_code(137276512, 3, 83)
rfdevice.tx_code(17061062, 1, 190)
rfdevice.tx_code(17061272, 3, 83)
rfdevice.tx_code(4265267, 1, 190)
rfdevice.cleanup()
