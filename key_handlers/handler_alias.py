from handler_base import TextReplacement, BaseKeyHandler

import json

class AliasKeyHandler(BaseKeyHandler):
    
    # Dictionary of aliases
    aliasReplacements = {}

    # Constructor - Populate aliases
    def __init__(self, configFile):
        if configFile:
            self.populateAliases(configFile)

    # Populate aliases from config file
    def populateAliases(self, configFile):

        with open(configFile) as data_file:
            data = json.load(data_file)

        # Will throw exception if aliases key does not exist.
        # This will be caught above and this key handler won't run
        configReplacements = data['aliases']

        for alias in configReplacements:
            self.aliasReplacements[alias] = configReplacements[alias]


    # Return text match if any exists
    def getTextReplacement(self, keyEvent):

        print keyEvent

        # If backspace, decrease all positions by 1
        if keyEvent.Ascii == 0 and len(self.currentKeyString) > 0:
            self.currentKeyString = self.currentKeyString[:-1]
            return False, None

        # Process key
        currentChar = chr(keyEvent.Ascii)

        # Iterate 
        for alias in self.aliasReplacements:            
            if alias in self.currentKeyString:
                return True, TextReplacement(alias, self.aliasReplacements[alias])

        return False, None