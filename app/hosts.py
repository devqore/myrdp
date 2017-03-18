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

    def getGroupsList(self):
        """
        :return: list with group names
        """
        return sum(self._db.session.query(HostTable.group).filter(HostTable.group.isnot(None)).distinct(), ())

    def getFilteredHostsNames(self, queryFilter=None):
        def q(): return self._db.session.query(HostTable.name)
        if queryFilter:
            hostsList = q().filter(HostTable.name.like("%%%s%%" % queryFilter))
        else:
            hostsList = q()
        return sorted(sum(hostsList, ()))

    def updateHostValues(self, host, values):
        """
        :param host: host object
        :param values: Dictionary {attribute: value}
        """
        self._db.updateObject(host, values)

    def create(self, name, address, user=None, password=None, group=None):
        host = HostTable(name=name, address=address, user=user, password=password, group=group)
        self._db.createObject(host)
        return host

    def delete(self, hostName):
        host = self.get(hostName=hostName)
        self._db.deleteObject(host)
