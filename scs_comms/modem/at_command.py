'''
Created on 28 Dec 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
'''


# --------------------------------------------------------------------------------------------------------------------

class ATCommand(object):
    '''
    classdocs
    '''

    DEFAULT_TIMEOUT =       1

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct(cls, text):
        pieces = text.split("|")

        # cmd...
        cmd = pieces[0].strip()

        # timeout...
        if len(pieces) > 1:
            field = pieces[1].strip()
            timeout = float(field) if len(field) > 0 else None
        else:
            timeout = cls.DEFAULT_TIMEOUT

        # attempts...
        if len(pieces) > 2:
            field = pieces[2].strip()
            attempts = int(field) if len(field) > 0 else 1
        else:
            attempts = 1

        return ATCommand(cmd, timeout, attempts)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, cmd, timeout, attempts=1):
        '''
        Constructor
        '''
        self.__cmd = cmd
        self.__timeout = timeout
        self.__attempts = attempts


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def cmd(self):
        return self.__cmd


    @property
    def timeout(self):
        return self.__timeout


    @property
    def attempts(self):
        return self.__attempts


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "ATCommand:{cmd:%s, timeout:%0.3f, attempts:%d}" % \
                    (self.cmd, self.timeout, self.attempts)
