import json


class TextReplacement:

    def __init__(self, removeLength, text):
        self.removeLength = removeLength
        self.text = text


class BaseKeyHandler(object):

    currentKeyString = ''

    def getTextReplacement(self, key):
        print 'Error. getTextReplacement() is unimplemented.'

    def reset(self):
        currentKeyString = ''
