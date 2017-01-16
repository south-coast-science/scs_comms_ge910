'''
Created on 27 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''

import time

import Adafruit_BBIO.GPIO as GPIO

from scs_comms.modem.at_command import ATCommand
from scs_comms.modem.at_response import ATResponse

from scs_host.lock.lock import Lock
from scs_host.sys.host_gpi import HostGPI
from scs_host.sys.host_gpo import HostGPO
from scs_host.sys.host_serial import HostSerial


# --------------------------------------------------------------------------------------------------------------------

class GE910(object):
    '''
    Telit GE910 GSM modem
    '''

    ON_OFF =            "P8_39"         # active high
    HW_SHUTDOWN =       "P8_40"         # active high

    VAUX =              "P8_43"         # active low

    GPIO_02 =           "P8_46"
    GPIO_03 =           "P8_45"

    UART =              4

    __BAUD_RATE =       115200

    __LOCK_PWR =        "PWR"
    __LOCK_TX =         "TX"

    __SERIAL_TIMEOUT =  10.0
    __LOCK_TIMEOUT =    60.0


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, use_led):
        self.__use_led = use_led

        self.__pwmon = HostGPI(GE910.VAUX)

        self.__serial = None


    # ----------------------------------------------------------------------------------------------------------------

    def switch_on(self):
        # lock...
        Lock.acquire(self.__lock_name(GE910.__LOCK_PWR), GE910.__LOCK_TIMEOUT, False)

        # GPIO...
        self.__on_off = HostGPO(GE910.ON_OFF, GPIO.LOW)
        self.__hw_shutdown = HostGPO(GE910.HW_SHUTDOWN, GPIO.LOW)

        self.__serial = HostSerial(GE910.UART, GE910.__BAUD_RATE, True)

        # power...
        self.__on_off.state = GPIO.HIGH
        time.sleep(6)

        self.__on_off.state = GPIO.LOW
        time.sleep(1)

        # TODO: test pwmon

        # LED...
        if not self.__use_led:
            return

        cmd = ATCommand("AT#SLED=1", 1.0)
        self.execute(cmd)


    def switch_off(self):
        # power...
        self.__on_off.state = GPIO.HIGH
        time.sleep(3)

        self.__on_off.state = GPIO.LOW
        time.sleep(1)

        # TODO: test pwmon

        # GPIO...
        self.__serial = None

        # lock...
        self.end_tx()
        Lock.release(self.__lock_name(GE910.__LOCK_PWR))


    # ----------------------------------------------------------------------------------------------------------------

    def start_tx(self):
        Lock.acquire(self.__lock_name(GE910.__LOCK_TX), GE910.__LOCK_TIMEOUT, False)


    def end_tx(self):
        Lock.release(self.__lock_name(GE910.__LOCK_TX))


    # ----------------------------------------------------------------------------------------------------------------

    def execute(self, command):
        try:
            self.__serial.open(GE910.__SERIAL_TIMEOUT)

            response = None
            time.sleep(0.3)

            for i in range(command.attempts):
                if i > 0:
                    time.sleep(command.timeout)

                if command.cmd.startswith("UR"):
                    terminators = [command.cmd[2:]]
                else:
                    terminators = ATResponse.RESULT_CODES
                    self.__serial.write_line(command.cmd)
                    time.sleep(0.1)

                lines = self.__read_text(terminators, command.timeout)
                response = ATResponse.construct(lines)

                if len(terminators) == 1 or response.code == "OK":
                    break

            return response

        finally:
            self.__serial.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __read_text(self, terminators, timeout):
        end_time = time.time() + timeout

        text = []
        while True:
            if time.time() > end_time:
                break

            line = self.__serial.read_line(HostSerial.EOL, timeout)

            if len(line) == 0:
                continue

            text.append(line)

            for terminator in terminators:
                if line == terminator or (terminator.startswith("#") and line.startswith(terminator)):
                    return text

        return text


    def __lock_name(self, func):
        return GE910.__name__ + "-" + func


    # ----------------------------------------------------------------------------------------------------------------

    def is_on(self):
        return Lock.exists(self.__lock_name(GE910.__LOCK_PWR))


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pwmon(self):
        return self.__pwmon.state


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "GE910:{use_led:%s, pwmon:%s, serial:%s}" % (self.__use_led, self.pwmon, self.__serial)
