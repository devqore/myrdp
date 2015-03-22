# -*- coding: utf-8 -*-
import os
from sqlalchemy.exc import IntegrityError
from unittest import TestCase

from app.config import Config
from app.database import Database
from app.database.schema import HostTable
from app.hosts import Hosts

J = os.path.join
CONFIG_FILE = J(os.path.dirname(__file__), 'test_config.yaml')
C = Config(CONFIG_FILE)


class ConfigTests(TestCase):

    def assertPath(self, path):
        try:
            c = Config(path)
        except IOError as e:
            self.fail(unicode(e))
        c._drop()

    def test_absPath(self):
        self.assertPath(CONFIG_FILE)

    def test_relativePath(self):
        # path is always relative to conf dir
        configPath = J("..", "tests", 'test_config.yaml')
        self.assertPath(configPath)


class DatabaseTests(TestCase):
    def test_db(self):
        db = Database(C.getConnectionString())
        db.recreate()
        rm = HostTable(name="xyz", address="192.168.6.66", user="abc", password="abc")
        db.session.add(rm)


class HostsTests(TestCase):
    def test_hosts(self):
        db = Database(C.getConnectionString())
        db.recreate()
        hosts = Hosts(db)

        h1 = hosts.create(u"test1", u"192.168.6.66")
        h2 = hosts.create(u"test2", u"192.168.6.77", u"ąść", u"password")

        allHosts = hosts.getAllHostsNames()
        self.assertListEqual([u"test1", u"test2"], allHosts)
        h2.user = u"łęść"

        # get once again host from database and asert its modified
        h2bis = hosts.get(u"test2")
        self.assertEqual(u"łęść", h2bis.user)

        # fields required
        self.assertRaises(IntegrityError, hosts.create,
                          None, None, None, None)
