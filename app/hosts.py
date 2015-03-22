# -*- coding: utf-8 -*-
from app.database.schema import HostTable


class Hosts(object):
    def __init__(self, database):
        """
        :param database: Database instance app.database.Database
        :type database: app.database.Database
        """
        self._db = database

    def get(self, hostName):
        return self._db.getObjectByName(HostTable, hostName)

    def getAllHostsNames(self):
        """
        :return: list with host names
        """
        hostsList = sum(self._db.session.query(HostTable.name), ())
        return sorted(hostsList)

    def create(self, name, address, user=None, password=None):
        host = HostTable(name=name, address=address, user=user, password=password)
        self._db.createObject(host)
        return host

    def delete(self, hostName):
        host = self.get(hostName=hostName)
        self._db.deleteObject(host)
