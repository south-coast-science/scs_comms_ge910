#!/usr/bin/env python3

"""
Created on 20 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

command line example:
./scs_comms/modem_power.py -v 1
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_comms.modem.modem import Modem
from scs_comms.cmd.cmd_power import CmdPower

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    I2C.open(Host.I2C_SENSORS)

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdPower()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resource...

        modem = Modem(True)

        if cmd.verbose:
            print(modem, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        if cmd.set() and cmd.power != modem.power:
            if cmd.power:
                modem.switch_on()
            else:
                modem.switch_off()

        print(modem.power)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        I2C.close()
