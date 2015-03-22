# -*- coding: utf-8 -*-
from app import logging


class Client(object):

    def __init__(self, executable, args):
        """
        :param executable: executable command/path
        :param args: raw options for given client
        :return:
        """
        self.executable = executable
        self.args = args.split(" ")
        self.settings = {}  # dictionary to store client settings

    def setWindowParameters(self, windowId, width, height):
        raise NotImplementedError

    def setUserAndPassword(self, user, password):
        raise NotImplementedError

    def setAddress(self, address):
        raise NotImplementedError

    def getComposedCommand(self):
        raise NotImplementedError


class RdesktopClient(Client):
    """ todo: at this time only freerdp implemented """
    pass


class FreerdpClient(Client):

    def setWindowParameters(self, windowId, width, height):
        self.settings.update({"parent-window": int(windowId), "w": width, "h": height})

    def setUserAndPassword(self, user=None, password=None):
        if user:
            self.settings['u'] = user
        if password:
            self.settings['p'] = password

    def setAddress(self, address):
        self.settings['v'] = address

    def getComposedCommand(self):
        """ Compose command with set earlier params
        :return: execCmd and optsList
        """
        argsList = ["/%s:%s" % (k, v) for k, v in self.settings.items()]
        argsList.extend(self.args)
        logging.debug("Running command:\n%s %s" % (self.executable, " ".join(argsList)))
        return self.executable, argsList


def ClientFactory(clientType, *args, **kwargs):
    """ Creates proper remote desktop client for given parameters """
    clientTypeToClass = {
        "xfreerdp": FreerdpClient,
        "rdesktop": RdesktopClient
    }
    return clientTypeToClass[clientType](*args, **kwargs)



