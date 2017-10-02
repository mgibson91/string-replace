import json

from common.utils import tryCastToInt, getBoolValueFromDictionary, getIntValueFromDictionary

class TextReplacement:

    def __init__(self, removeLength, text):
        self.removeLength = removeLength
        self.text = text


class BaseKeyHandler(object):

    currentKeyString = ''

    # Base handler constructor. Processes config and delegates to handler subclass 'updateConfig()'
    def __init__(self, configFile):

        with open(configFile) as jsonConfig:
            data = json.load(jsonConfig)

        if 'general' in data:
            self.processGeneralConfigOptions(data['general'])

        # Apply any general config specified by plugin
        pluginData = self.getPluginConfig(data)
        if pluginData and 'general' in pluginData:
            self.processGeneralConfigOptions(pluginData['general'])

        # Call subclass implementation for specific config updates
        self.updateConfig(pluginData)
        self.displayConfig()

    # Process general config options. These can be overwritten by handler subclasses
    def processGeneralConfigOptions(self, config):

        if not config:
            return

        if 'tabCharacters' in config:
            self.tabCharacters = getIntValueFromDictionary(config, 'tabCharacters', 1)

        if 'keyBufferLimit' in config:
            self.keyBufferLimit = getIntValueFromDictionary(config, 'keyBufferLimit', 20)

        if 'debug' in config:
            self.debug = getBoolValueFromDictionary(config, 'debug', False)

    def displayConfig(self):

        self.logInfo('{} handler config:\n'.format(self.getName()))
        self.logInfo('Tab characters: {}'.format(self.tabCharacters))
        self.logInfo('key buffer limit: {}'.format(self.keyBufferLimit))
        self.logInfo('Debug: {}\n'.format(self.debug))
        

    def checkForTextReplacement(self, key):
        print 'Error. getTextReplacement() is unimplemented for this key handler'

    def updateConfig(self, config):
        print 'Error. updateConfig() unimplemented for this key handler'

    # Returns plugin specific data using the name of each handler / plugin 
    def getPluginConfig(self, config):

        if config and 'plugins' in config:   
            for plugin in config['plugins']:
                if self.getName().lower() in plugin['name'].lower():
                    return plugin

        return None

    def getName(self):
        print 'Error. getName() is unimplemented for this key handler'

    def logInfo(self, message):
        print message

    def logDebug(self, message):
        if (self.debug):
            print message

    def reset(self):
        self.currentKeyString = ''
