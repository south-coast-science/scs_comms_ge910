#!/usr/bin/env python3

"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_comms.modem.modem import Modem

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    modem = Modem(True)
    print(modem)

    modem.switch_on()


except KeyboardInterrupt:
    print("modem_test: terminated", file=sys.stderr)

finally:
    I2C.close()
