#!/usr/bin/env python3

"""
Created on 27 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys
import time

from scs_comms.modem.at_command import ATCommand
from scs_comms.modem.ge910 import GE910


# --------------------------------------------------------------------------------------------------------------------

print("modem...")
modem = GE910(True)
print(modem)
print("-")

command = ATCommand.construct("")

try:
    print("on...")
    modem.switch_on()
    print(modem)
    print("-")

    print("cmd...")

    while True:
        print("> ", end="")
        sys.stdout.flush()

        text = sys.stdin.readline().strip()
        sys.stdin.flush()

        if len(text) > 0:
            command = ATCommand.construct(text)     # use previous command on empty text

        comman_start_time = time.time()
        response = modem.execute(command)
        print(response)
        print("-")

        command_time = time.time() - comman_start_time
        print("cmd time: %6.3f" % command_time)
        print("")

except KeyboardInterrupt as ex:
    print("ge90_test: KeyboardInterrupt", file=sys.stderr)

finally:
    print("off...")
    modem.switch_off()
    print(modem)
    print("-")

