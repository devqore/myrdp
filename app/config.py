# -*- coding: utf-8 -*-
import os
import logging
import yaml

from app.utils import Singleton

J = os.path.join


class Config():
    """ Singleton class to manage configuration """

    __metaclass__ = Singleton

    def __init__(self, configFile):
        """
        :param configFile: Absolute path to config file or file name (from conf dir)
        :return:
        """
        if os.path.isabs(configFile):
            self.config = configFile
        else:
            configDir = J(os.path.dirname(__file__), "..", "conf")
            self.config = J(configDir, configFile)

        with open(self.config, 'r') as f:
            self.data = yaml.load(f)

    def getGlobalOption(self, option):
        try:
            return self.data['global'][option]
        except KeyError:
            logging.error("Option '%s' not found in config file '%s'" % (option, self.config))

    def getConnectionString(self):
        return self.getGlobalOption('connection_string')

    def getLogLevel(self):
        return self.getGlobalOption('log_level')

    def getRdpClient(self):
        clientType = self.getGlobalOption('client')
        return clientType, self.data[clientType]

    def _drop(self):
        """ Used only for test purposes """
        Singleton(self)._instances = {}