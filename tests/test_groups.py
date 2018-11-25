# -*- coding: utf-8 -*-
from tests import BaseTestCase


class GroupTestCase(BaseTestCase):
    def setUp(self):
        super(GroupTestCase, self).setUp()
        self.groups = self.hosts.groups

    def testAddGroupWithHost(self):
        self.hosts.create("a", "b", "c", "d", group="e")
        host = self.hosts.get("a")
        self.assertEqual("e", host.group)

    def testDefaultGroupPassword(self):
        group = self.groups.create("some_group", defaultPassword="aa")
        self.hosts.create("default_password", address="a", user="u1", group=group.name)
        host = self.hosts.get("default_password")
        self.assertEqual(host.password, "aa")
        self.assertEqual(host.user, "u1")

    def testDefaultGroupUser(self):
        group = self.groups.create("other_group", defaultUsername="usi")
        self.hosts.create("default_user", address="b", password="pass", group=group.name)
        host = self.hosts.get("default_user")
        self.assertEqual(host.password, "pass")
        self.assertEqual(host.user, "usi")

    def testOverrideUserAndPassword(self):
        group = self.groups.create("ignored", defaultUsername="ignored_user", defaultPassword="ignored_passwd")
        self.hosts.create("override", address="x", user="u", password="p", group=group.name)
        host = self.hosts.get("override")
        self.assertEqual(host.password, "p")
        self.assertEqual(host.user, "u")