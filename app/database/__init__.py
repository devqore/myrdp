# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import Config
from app.database.schema import Base


class Database(object):

    def __init__(self, engineString=None, echo=False):
        """
        :param engineString: at this time only sqlite, e.g: sqlite:////some/location.sqlite,
        if None, connection string from config will be used
        """
        if not engineString:
            engineString = Config().getConnectionString()
        self.engine = create_engine(engineString, echo=echo)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.metadata = Base.metadata
        self.metadata.bind = self.engine  # bind or not to bind ?

    def create(self):
        self.metadata.create_all()

    def drop(self):
        self.metadata.drop_all()

    def recreate(self):
        self.drop()
        self.create()

    def getObjectByName(self, schemaType, objectName):
        """
        :param schemaType:
        :param objectName:
        :return:
        """
        obj = self.session.query(schemaType).filter_by(name=objectName).first()
        return obj

    def tryCommit(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def createObject(self, schemaObject):
        self.session.add(schemaObject)
        self.tryCommit()

    def deleteObject(self, schemaObject):
        self.session.delete(schemaObject)
        self.tryCommit()

    def updateObject(self, schemaObject, values):
        for attr, value in values.items():
            setattr(schemaObject, attr, value)
        self.tryCommit()