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
    def updateConfig(self, aliasConfig):      

        self.logDebug('Updating alias config\n')

        # It is ok to fail with an exception here. It means this handler won't be used
        configReplacements = aliasConfig['data']

        for alias in configReplacements:
            self.aliasReplacements[alias] = configReplacements[alias]

    # Return text match if any exists
    def getTextReplacement(self, character):
      
        # Iterate 
        for alias in self.aliasReplacements:  

            if alias in self.currentKeyString:
                return True, TextReplacement(len(alias), self.aliasReplacements[alias])        

        return False, None

    