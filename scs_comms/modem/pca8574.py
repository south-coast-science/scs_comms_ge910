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
    __CMD_RESET =           0x30a2
    __CMD_CLEAR =           0x3041

    __CMD_READ_SINGLE =     0x2c06
    __CMD_READ_STATUS =     0xf32d


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

    def reset(self):
        try:
            I2C.start_tx(self.__addr)
            I2C.write16(PCA8574.__CMD_RESET)
            time.sleep(0.001)

            I2C.write16(PCA8574.__CMD_CLEAR)
            time.sleep(0.001)

        finally:
            I2C.end_tx()


    def sample(self):
        try:
            I2C.start_tx(self.__addr)
            temp_msb, temp_lsb, _, humid_msb, humid_lsb, _ = I2C.read_cmd16(PCA8574.__CMD_READ_SINGLE, 6)

            raw_humid = (humid_msb << 8) | humid_lsb
            raw_temp = (temp_msb << 8) | temp_lsb

            return SHTDatum(PCA8574.humid(raw_humid), PCA8574.temp(raw_temp))

        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def status(self):
        try:
            I2C.start_tx(self.__addr)
            status_msb, status_lsb, _ = I2C.read_cmd16(PCA8574.__CMD_READ_STATUS, 3)

            return (status_msb << 8) | status_lsb

        finally:
            I2C.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PCA8574:{addr:0x%02x}" % self.__addr
