# -*- coding: utf-8 -*-
from ConfigParser import ConfigParser
from os.path import abspath
import sys

class Config(ConfigParser):
    
    def __init__(self, config):
        ConfigParser.__init__(self)
        self.read(config)
        sections = self.sections()
        try:
            self.globalConfig = sections.pop(sections.index("GlobalConfig"))
        except ValueError:
            print "Section [GlobalConfig] not found in file config.ini"
            sys.exit(1)
        
        self.filePath = abspath(config) 
        
        self.hosts = sections
    
    def getUniqueHost(self, host):
        host = str(host)#we have QString
        if not self.has_section(host):
            return host
        
        i = 1
        while True:
            newSectionName = "%s_%i" % (host, i)
            if self.has_section(newSectionName):
                i += 1
                continue
            return newSectionName
        
        

    def addHost(self, host, optionsDict):
        self.add_section(host)
        
        for k,v in optionsDict.items():
            self.set(host, k, v)
    
    def getGlobalConfig(self):
        return dict(self.items(self.globalConfig))
    
    def getHostOptions(self, host):
        #using global config as template and updating values 
        template = self.getGlobalConfig()
        template.update(dict(self.items(host)))
        return template
    
        