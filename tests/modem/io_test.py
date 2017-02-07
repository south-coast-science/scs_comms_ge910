#!/usr/bin/env python3

"""
Created on 6 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_comms.modem.io import IO
from scs_comms.modem.pca8574 import PCA8574State

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

I2C.open(Host.I2C_SENSORS)

try:
    io = IO(IO.filename(Host))
    print(io)

    state = PCA8574State.load_from_file(IO.filename(Host))
    print(state)

    print("power:%s" % io.power)

    io.power = not io.power
    print("power:%s" % io.power)

    state = PCA8574State.load_from_file(IO.filename(Host))
    print(state)

finally:
    I2C.close()
