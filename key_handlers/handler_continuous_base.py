from handler_base import TextReplacement, BaseKeyHandler

import json

# This base handler contains a rolling buffer of the last <keyBufferLimit> characters.
# 
# It provides a hook method getTextReplacement(character) where a user can simply add plugins.
class BaseContinuousKeyHandler(BaseKeyHandler):

    # Constructor
    def __init__(self, configFile):
        super(BaseContinuousKeyHandler, self).__init__(configFile)

    def updateCurrentTextString(self, character):

        if len(self.currentKeyString) == self.keyBufferLimit:
            self.currentKeyString = self.currentKeyString[1:self.keyBufferLimit]

        self.currentKeyString += character

    # Returns true if special character has been handled.
    def handleSpecialCharacters(self, keyEvent):

        # If backspace, decrease all positions by 1
        if keyEvent.Key == 'BackSpace' and len(self.currentKeyString) > 0:
            self.currentKeyString = self.currentKeyString[:-1]
            return True

        # Add the number of characters specified in config.
        # If the current application uses the tab character, this should be set to 1
        # Otherwise, tabCharacters should be equal to the number of spaces inserted by tab
        if keyEvent.Key == 'Tab':

            for _ in range(self.tabCharacters):
                self.updateCurrentTextString(' ')
            return True

        return False

    #########################################################################################################
    # NOTE: This is the method that needs to be overwritten to easily reuse the base continuous key handler #
    #########################################################################################################
    def getTextReplacement(self, character):
        print 'Error. getTextReplacement is unimplemented for this key handler'
        return False, None

    # Return text match if any exists
    def checkForTextReplacement(self, keyEvent):

        if not self.handleSpecialCharacters(keyEvent):
            self.updateCurrentTextString(chr(keyEvent.Ascii))
      
        return self.getTextReplacement(chr(keyEvent.Ascii))

    