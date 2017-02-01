"""
Created on 1 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------


class PCA8574(object):
    """
    NXP remote 8-bit I/O expander
    """
    _ADDR =                 0x38            # PCA8574: 0x30 + addr, PCA8574A: 0x38 + addr


    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def humid(raw_humid):
        humid = raw_humid / 65535.0

        return 100.0 * humid


    @staticmethod
    def temp(raw_temp):
        temp = raw_temp / 65535.0

        return -45.0 + (175.0 * temp)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, addr):
        """
        Constructor
        """
        self.__addr = addr

        self.__raw_temperature = None
        self.__raw_humidity = None


    # ----------------------------------------------------------------------------------------------------------------



    # ----------------------------------------------------------------------------------------------------------------


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PCA8574:{addr:0x%02x}" % self.__addr
