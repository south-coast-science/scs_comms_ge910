"""
Created on 27 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from collections import OrderedDict

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class ATResponse(JSONable):
    """
    classdocs
    """

    RESULT_CODES = ['OK', 'ERROR', 'CONNECT', 'NO CARRIER']

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, lines):
        if len(lines) < 1:
            return ATResponse(None, None, None)

        if len(lines) < 2:
            return ATResponse(lines[0], None, None)

        return ATResponse(lines[0], lines[1:-1], lines[-1])


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cmd, items, code):
        """
        Constructor
        """
        self.__cmd = cmd
        self.__items = items
        self.__code = code


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['cmd'] = self.cmd
        jdict['items'] = self.items
        jdict['code'] = self.code

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cmd(self):
        return self.__cmd


    @property
    def items(self):
        return self.__items


    @property
    def code(self):
        return self.__code


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ATResponse:{cmd:%s, items:%s, code:%s}" % (self.cmd, self.items, self.code)
