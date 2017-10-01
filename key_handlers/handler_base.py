import json

from common.utils import tryCastToInt, getBoolValueFromDictionary, getIntValueFromDictionary

class TextReplacement:

    def __init__(self, removeLength, text):
        self.removeLength = removeLength
        self.text = text


class BaseKeyHandler(object):

    currentKeyString = ''

    def __init__(self, configFile):

        with open(configFile) as jsonConfig:
            data = json.load(jsonConfig)

        general = data['general']

        self.tabCharacters = getIntValueFromDictionary(general, 'tabCharacters', 1)
        self.keyBufferLimit = getIntValueFromDictionary(general, 'keyBufferLimit', 20)
        self.debug = getBoolValueFromDictionary(general, 'debug', False)

        print """
General config
    Tab characters: {}
    Key buffer limit: {}
    Debug: {}\n""".format(self.tabCharacters, self.keyBufferLimit, self.debug)

        # Call subclass implementation for specific config updates
        self.updateConfig(configFile)

    def checkForTextReplacement(self, key):
        print 'Error. getTextReplacement() is unimplemented for this key handler'

    def updateConfig(self, config):
        print 'Error. updateConfig() unimplemented for this key handler'

    def getName(self):
        print 'Error. getName() is unimplemented for this key handler'

    def logDebug(self, message):
        if (self.debug):
            print message

    def reset(self):
        self.currentKeyString = ''
