from ConfigParser import ConfigParser
import sys

class Config(ConfigParser):
    
    def __init__(self):
        ConfigParser.__init__(self)
        self.read("config.ini")
        sections = self.sections()
        try:
            self.globalConfig = sections.pop(sections.index("GlobalConfig"))
        except ValueError:
            print "Section [GlobalConfig] not found in file config.ini"
            sys.exit(1)
        
        self.hosts = sections
        
    def getHostOptions(self, host):
        #using global config as template and updating values 
        template = dict(self.items(self.globalConfig))
        template.update(dict(self.items(host)))
        return template