from handler_base import TextReplacement, BaseKeyHandler
from handler_continuous_base import BaseContinuousKeyHandler

import json

class AliasKeyHandler(BaseContinuousKeyHandler):

    # Dictionary of aliases
    aliasReplacements = {}

    # Constructor - Read config
    def __init__(self, configFile):
        super(AliasKeyHandler, self).__init__(configFile)

    def getName(self):
        return 'Alias'

    # Base class will call update config
    def updateConfig(self, configFile):      

        self.logDebug('Updating alias config')

        with open(configFile) as jsonConfig:
            data = json.load(jsonConfig)

        configReplacements = data['aliases']

        for alias in configReplacements:
            self.aliasReplacements[alias] = configReplacements[alias]

    # Return text match if any exists
    def getTextReplacement(self, character):

        if (self.debug):
            print 'currentKeyString: ' + self.currentKeyString
      
        # Iterate 
        for alias in self.aliasReplacements:  

            if alias in self.currentKeyString:
                return True, TextReplacement(len(alias), self.aliasReplacements[alias])        

        return False, None

    