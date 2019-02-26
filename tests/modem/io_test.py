#!/usr/bin/env python3

"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_comms.modem.io import IO
from scs_comms.modem.pca8574 import PCA8574State

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

filename = os.path.join(Host.lock_dir(), "dfe_io.json")

I2C.open(Host.I2C_SENSORS)

try:
    io = IO()
    print(io)

    state = PCA8574State.load_from_file(filename)
    print(state)

    print("power:%s" % io.power)

    io.power = not io.power
    print("power:%s" % io.power)

    state = PCA8574State.load_from_file(filename)
    print(state)

finally:
    I2C.close()
