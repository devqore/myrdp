# -*- coding: utf-8 -*-
import configparser
import logging
import os
import sys

from app.log import logger
from app.crypto import CryptoKey
from pathlib import Path

J = os.path.join


class Config(object):
    default_freerdp_args = "+clipboard /cert-ignore +drives " \
                           "/drive:home,/home -themes +compression " \
                           "/gdi:sw +auto-reconnect"
    settings_file_path = J(Path.home(), '.config', 'myrdp', 'settings.conf')

    def __init__(self):
        os.makedirs(self.config_directory, exist_ok=True)
        self.config = configparser.ConfigParser()
        self.config['General'] = {
            'freerdp_arguments': self.default_freerdp_args,
            'logging_level': 'error',
            'freerdp_executable': 'xfreerdp',
            'database_location': J(self.config_directory, 'myrdp.sqlite')
        }

        if not os.path.isfile(self.settings_file_path):
            self.write_config()

        self.config.read(self.settings_file_path)

    def write_config(self):
        with open(self.settings_file_path, 'w') as configfile:
            self.config.write(configfile)

    @property
    def settings(self):
        return None

    def set_value(self, setting, value, section='General'):
        self.config[section][setting] = value
        self.write_config()

    def get_value(self, setting, defaultValue=None, section='General'):
        return self.config[section].get(setting, defaultValue)

    def get_boolean_value(self, setting, defaultValue):
        value = self.settings.value(setting, defaultValue)
        if isinstance(value, bool):
            return value
        return value.lower() in ("yes", "true", "1")

    @property
    def main_directory(self):
        # pyinstaller sets sys.frozen attribute
        if getattr(sys, 'frozen', False):
            mainDirectory = os.path.dirname(sys.executable)
        else:
            mainDirectory = J(os.path.dirname(__file__), "..")
        return mainDirectory

    @property
    def config_directory(self):
        return os.path.dirname(self.settings_file_path)

    @property
    def database_location(self):
        defaultLocation = J(self.config_directory, "myrdp.sqlite")
        location = self.get_value('database_location', defaultLocation)
        if location == '':
            location = defaultLocation
        return location

    def set_database_location(self, location):
        self.set_value('database_location', location)

    def get_connection_string(self):
        connectionString = "sqlite:///%s" % self.database_location
        logging.debug(connectionString)
        return connectionString

    @property
    def freerdp_args(self):
        args = self.get_value('freerdp_arguments', self.default_freerdp_args)
        return args

    def set_freerdp_args(self, freerdpArgs):
        self.set_value('freerdp_arguments', freerdpArgs)

    @property
    def freerdp_executable(self):
        return self.get_value('freerdp_executable', 'xfreerdp')

    def set_freerdp_executable(self, freerdpExecutable):
        self.set_value('freerdp_executable', freerdpExecutable)

    @property
    def log_level(self):
        return str(self.get_value('logging_level', "error"))

    def set_log_level(self, loggingLevel=None):
        if loggingLevel:
            self.set_value('logging_level', loggingLevel)
        logger.setLevel(getattr(logging, self.log_level.upper()))

    @property
    def logging_levels(self):
        return ["error", "debug"]

    def get_rdp_client(self):
        data = {
            "executable": self.freerdp_executable,
            "args": self.freerdp_args
        }
        return "xfreerdp", data

    @property
    def private_key_path(self):
        return J(self.config_directory, 'private.key')

    def get_private_key(self, passphrase=None):
        ck = CryptoKey()
        if os.path.exists(self.private_key_path):
            ck.load(self.private_key_path, passphrase)
        else:  # if private key doesn't exist, then save generated one
            ck.save(self.private_key_path, passphrase)
        return ck
