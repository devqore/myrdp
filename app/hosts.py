# -*- coding: utf-8 -*-
from collections import OrderedDict
from app.log import logger
from sqlalchemy import or_
from sqlalchemy.sql.expression import case, collate

from app.database.schema import HostTable


class Hosts(object):
    def __init__(self, database, crypto):
        """
        :param database: Database instance app.database.Database
        :type database: app.database.Database
        :param crypto: crypto object used to password encryption
        :type crypto: app.crypto.CryptoKey
        """
        self._db = database
        self._crypto = crypto

    def get(self, hostName):
        hostTable = self._db.getObjectByName(HostTable, hostName)
        if hostTable is None:
            raise LookupError(u"Host not found")
        return Host(hostTable, self._crypto)

    def getAllHostsNames(self):
        """
        :return: list with host names
        """
        hostsList = sum(self._db.session.query(HostTable.name), ())
        return sorted(hostsList)

    def getHostsListByHostNameAndGroup(self, hostFilter=None, groupFilter=None):
        result = self._db.session.query(
            HostTable.name).order_by(
            collate(HostTable.name, 'NOCASE')
        ).filter(
            or_(HostTable.group.in_(groupFilter), HostTable.group.is_(None))  # always include hosts without groups
        )

        if hostFilter:
            result = result.filter(HostTable.name.like(u"%%{}%%".format(hostFilter)))

        return sum(result, ())

    def getGroupsList(self):
        """
        :return: list with group names
        """
        return sum(self._db.session.query(HostTable.group).filter(HostTable.group.isnot(None)).distinct(), ())

    def getGroupedHostNames(self, queryFilter=None):
        hostsList = self._db.session.query(HostTable.name, HostTable.group).order_by(
            case([(HostTable.group == None, 1)], else_=0),  # nulls last
            collate(HostTable.group, 'NOCASE'),
            collate(HostTable.name, 'NOCASE')
        )

        if queryFilter:
            hostsList = hostsList.filter(HostTable.name.like("%%%s%%" % queryFilter))

        groupedHosts = OrderedDict()
        for host, group in hostsList:
            if group in groupedHosts.keys():
                groupedHosts[group].append(host)
            else:
                groupedHosts[group] = [host]
        return groupedHosts

    def updateHostValues(self, host, values):
        """
        :param host: host object
        :param values: Dictionary {attribute: value}
        """
        passwd = values.get('password')
        if passwd:
            values["password"] = self._crypto.encrypt(passwd)
        self._db.updateObject(host.ctx, values)

    def create(self, name, address, user, password, group=None):
        if password:
            password = self._crypto.encrypt(password)
        host = HostTable(name=name, address=address, user=user, password=password, group=group)
        self._db.createObject(host)
        return Host(host, self._crypto)

    def delete(self, hostName):
        host = self.get(hostName=hostName)
        self._db.deleteObject(host)


class Host(object):
    def __init__(self, hostTable, crypto):
        self.ctx = hostTable
        self._crypto = crypto

    def __getattr__(self, item):
        return self.ctx.__dict__.get(item)

    def setValue(self, key, value):
        return self.ctx.__setattr__(key, value)

    @property
    def password(self):
        if self.ctx.password:
            try:
                return self._crypto.decrypt(self.ctx.password)
            except ValueError as e:
                logger.error(u"Couldn't decrypt password. {}".format(e.message))
            except TypeError as e:
                logger.error(u"Couldn't decode base64 password. {}".format(e.message))
        return None
