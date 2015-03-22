# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HostTable(Base):
    __tablename__ = 'hosts'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)
    user = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<name='%s', address='%s', user='%s', password='%s'>" \
               % (self.name, self.address, self.user, self.password)
