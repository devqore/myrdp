# -*- coding: utf-8 -*-
from unittest import TestCase
from app.crypto import CryptoKey
from app.database import Database
from app.hosts import Hosts


class HostsTestCase(TestCase):
    def setUp(self):
        self.db = Database('sqlite://')  # in memory database
        self.db.create()
        self.ck = CryptoKey()
        self.hosts = Hosts(self.db, self.ck)

    def tearDown(self):
        self.db.drop()

    def test_password(self):
        self.hosts.create("first host", "address", "user", "password")
        host1 = self.hosts.get("first host")
        self.assertEqual(host1.password, "password")

        self.hosts.create("second host", "address", "user", password="differentpassword")
        host1 = self.hosts.get("first host")
        self.assertEqual(host1.password, "password")

        host2 = self.hosts.get("second host")
        self.assertEqual(host2.password, "differentpassword")

    def test_nonePassword(self):
        self.hosts.create("host", "address", None, None)
        host = self.hosts.get("host")
        self.assertIsNone(host.password)

    def test_updatePassword(self):
        host = self.hosts.create("host", "address", None, None)
        self.hosts.updateHostValues(host, {"password": "abc"})
        host = self.hosts.get("host")
        self.assertEqual(host.password, "abc")

        self.hosts.updateHostValues(host, {"password": "def"})
        host = self.hosts.get("host")
        self.assertEqual(host.password, "def")

        self.hosts.updateHostValues(host, {"password": None})
        host = self.hosts.get("host")
        self.assertIsNone(host.password)