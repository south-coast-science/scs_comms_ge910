"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import time

from scs_comms.modem.at_command import ATCommand
from scs_comms.modem.ge910 import GE910
from scs_comms.modem.pca8574 import PCA8574

from scs_host.lock.lock import Lock
from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

class Modem(object):
    """
    Modem with Telit GE910 and NXP PCA8574 remote 8-bit I/O expander
    """
    __PCA8574_ADDR =    0x38            # PCA8574: 0x30 + addr, PCA8574A: 0x38 + addr

    __LOCK_PWR =        "PWR"
    __LOCK_TIMEOUT =    60.0




    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __lock_name(cls, func):
        return cls.__name__ + "-" + func


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, use_led):
        """
        Constructor
        """
        self.__use_led = use_led

        self.__ge910 = GE910()
        self.__io = PCA8574(Modem.__PCA8574_ADDR)


    # ----------------------------------------------------------------------------------------------------------------

    def switch_on(self):
        # lock...
        Lock.acquire(self.__lock_name(Modem.__LOCK_PWR), Modem.__LOCK_TIMEOUT, False)

        # power
        self.__io.write(0xff)       # 1111 1111
        time.sleep(1)

        # serial...
        self.__serial = HostSerial(GE910.UART, GE910.__BAUD_RATE, True)

        # on_off...
        self.__io.write(0xf7)       # 1111 0111
        time.sleep(6)

        self.__io.write(0xff)       # 1111 1111
        time.sleep(1)

        # TODO: test pwmon

        # LED...
        if not self.__use_led:
            return

        cmd = ATCommand("AT#SLED=1", 1.0)
        self.execute(cmd)


    def switch_off(self):
        # on_off...
        self.__io.write(0xf7)       # 1111 0111
        time.sleep(6)

        self.__io.write(0xff)       # 1111 1111
        time.sleep(1)

        # TODO: test pwmon

        # GPIO...
        self.__serial = None

        # lock...
        self.__ge910.end_tx()
        Lock.release(self.__lock_name(Modem.__LOCK_PWR))


    # ----------------------------------------------------------------------------------------------------------------

    def execute(self, command):
        self.__ge910.execute(command)


    # ----------------------------------------------------------------------------------------------------------------

    def is_on(self):
        return Lock.exists(self.__lock_name(Modem.__LOCK_PWR))


    # ----------------------------------------------------------------------------------------------------------------

    # TODO: use of the io expander


    # ----------------------------------------------------------------------------------------------------------------

    def pwmon(self):
        pass            #TODO: implement pwmon()

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Modem:{ge910:%s, io:%s}" % (self.__ge910, self.__io)
