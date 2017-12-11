"""
Created on 20 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdPower(object):
    """unix command line handler"""

    def __init__(self):
        """stuff"""
        self.__parser = optparse.OptionParser(usage="%prog [1 | 0] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if len(self.__args) > 0:
            try:
                int(self.__args[0])
            except RuntimeError:
                return False

        return True


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.power is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def power(self):
        if len(self.__args) > 0:
            try:
                return int(self.__args[0])
            except RuntimeError:
                return None

        return None


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdPower:{power:%d, verbose:%s, args:%s}" % \
                    (self.power, self.verbose, self.args)
