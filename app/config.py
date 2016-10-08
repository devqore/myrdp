# -*- coding: utf-8 -*-
import logging
import os
import re
import sys
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
            configDir = J(self.mainDirectory, "conf")
            self.config = J(configDir, configFile)

        with open(self.config, 'r') as f:
            self.data = yaml.load(f)

    @property
    def mainDirectory(self):
        # pyinstaller sets sys.frozen attribute
        if getattr(sys, 'frozen', False):
            mainDirectory = os.path.dirname(sys.executable)
        else:
            mainDirectory = J(os.path.dirname(__file__), "..")
        return mainDirectory

    def getGlobalOption(self, option):
        try:
            return self.data['global'][option]
        except KeyError:
            logging.error("Option '%s' not found in config file '%s'" % (option, self.config))

    def getConnectionString(self):
        connectionString = self.getGlobalOption('connection_string')
        sqlitePrefix = "sqlite:///"
        databasePath = re.sub("^%s" % sqlitePrefix, "", connectionString)
        # if path is not absolute set path as relative path to main dir
        if not os.path.isabs(databasePath):
            connectionString = sqlitePrefix + J(self.mainDirectory, databasePath)
        return connectionString

    def getLogLevel(self):
        return self.getGlobalOption('log_level')

    def getRdpClient(self):
        clientType = self.getGlobalOption('client')
        return clientType, self.data[clientType]

    def _drop(self):
        """ Used only for test purposes """
        Singleton(self)._instances = {}