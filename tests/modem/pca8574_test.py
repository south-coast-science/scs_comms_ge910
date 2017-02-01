#!/usr/bin/env python3

"""
Created on 1 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_comms.modem.pca8574 import PCA8574

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)


try:
    pass

except KeyboardInterrupt:
    print("pca8574_test: terminated", file=sys.stderr)

finally:
    I2C.close()
