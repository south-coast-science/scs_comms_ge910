"""
Created on 3 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

useful commands:
ifup ppp0
ip a
ip route

ifdown ppp0
"""

import time

from scs_comms.modem.ge910 import GE910
from scs_comms.modem.io import IO

from scs_host.lock.lock import Lock


# TODO: separate board power control from modem power control

# --------------------------------------------------------------------------------------------------------------------

class Modem(object):
    """
    Modem with Telit GE910 and NXP PCA8574 remote 8-bit I/O expander
    """
    __LOCK_PWR =        "PWR"
    __LOCK_TIMEOUT =    60.0


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __lock_name(cls, func):
        return cls.__name__ + "-" + func


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__ge910 = GE910()
        self.__io = IO()


    # ----------------------------------------------------------------------------------------------------------------

    def switch_on(self):
        # lock...
        self.start_tx()

        # print("pwmon: %s" % self.__io.pwmon)

        # power...
        self.__io.power = IO.LOW
        self.__io.output_enable = IO.HIGH
        time.sleep(4)

        # switch on...
        self.__io.on_off = IO.LOW
        time.sleep(6)

        self.__io.on_off = IO.HIGH
        time.sleep(1)

        # TODO: test pwmon

        # print("pwmon: %s" % self.__io.pwmon)


    def switch_off(self):
        # print("pwmon: %s" % self.__io.pwmon)

        # switch off...
        # cmd = ATCommand("AT#SHDN", 1.0)
        # self.execute(cmd)

        end_time = time.time() + 5      # should be 15

        while True:
            # print("pwmon: %s" % self.__io.pwmon)

            if not self.__io.pwmon:
                break

            if time.time() > end_time:
                # print("HW_UNCONDITIONAL_SHUTDOWN")
                break

            time.sleep(1)

        # power...
        self.__io.output_enable = IO.LOW
        self.__io.power = IO.HIGH

        # lock...
        self.__ge910.end_tx()
        self.end_tx()


    # ----------------------------------------------------------------------------------------------------------------

    def setup_serial(self):
        self.__ge910.setup_serial()


    def execute(self, command):
        return self.__ge910.execute(command)


    # ----------------------------------------------------------------------------------------------------------------

    def start_tx(self):
        Lock.acquire(self.__lock_name(Modem.__LOCK_PWR), Modem.__LOCK_TIMEOUT)


    def end_tx(self):
        Lock.release(self.__lock_name(Modem.__LOCK_PWR))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power(self):
        return 1 if self.__io.power == IO.LOW else 0


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "Modem:{ge910:%s, io:%s}" % (self.__ge910, self.__io)
