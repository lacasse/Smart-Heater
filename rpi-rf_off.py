#!/usr/bin/env python3
from rpi_rf import RFDevice

rfdevice = RFDevice(17)
rfdevice.enable_tx()
rfdevice.tx_repeat = 1

rfdevice.tx_code(4265276, 1, 188)
rfdevice.tx_code(4265276, 1, 191)
rfdevice.tx_code(4265276, 1, 191)
rfdevice.tx_code(4265276, 1, 191)
rfdevice.cleanup()
