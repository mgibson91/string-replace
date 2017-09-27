import json

class TextReplacement:

    def __init__(self, removeLength, text):
        self.removeLength = removeLength
        self.text  = text 


class BaseKeyListener(object):

    def logKey(self, key):
        print 'log'


class AliasKeyListener(BaseKeyListener):

    # Dictionary of aliases
    # alias -> replacement
    aliasReplacements = {}

    # Dictionary of current positions
    # alias -> position
    aliasPositions = {}

    # Constructor - Populate aliases
    def __init__(self, configFile):
        if configFile:
            self.populateAliases(configFile)

    # Populate aliases from config file
    def populateAliases(self, configFile):

        with open(configFile) as data_file:
            data = json.load(data_file)

        if 'aliases' not in data:
            return 'No config file found.', {}

        configReplacements = data['aliases']

        for alias in configReplacements:
            self.aliasReplacements[alias] = configReplacements[alias]
            self.aliasPositions[alias]    = 0


    # Check for match
    def checkForMatch(self, keyEvent):

        # If backspace, decrease all positions by 1
        if keyEvent.Ascii == 0:
            for alias in self.aliasPositions:
                self.aliasPositions[alias] = max(0, (self.aliasPositions[alias] - 1))
            return False, None

        # Process key
        currentChar = chr(keyEvent.Ascii)

        # Iterate 
        for alias in self.aliasPositions:

            if alias[self.aliasPositions[alias]] == currentChar:
                self.aliasPositions[alias] += 1

                if self.aliasPositions[alias] == len(alias):
                    return True, TextReplacement(self.aliasPositions[alias], self.aliasReplacements[alias])
            else: 
                self.aliasPositions[alias] = 0 if (alias[0] != currentChar) else 1

        return False, None


    def logKey(self, keyEvent):        
        return self.checkForMatch(keyEvent)
