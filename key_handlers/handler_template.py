from handler_base import TextReplacement, BaseKeyHandler
from handler_continuous_base import BaseContinuousKeyHandler
from common.utils import tryCastToInt

import re
import json


class TemplateKeyHandler(BaseContinuousKeyHandler):

    templates = {}
    numTemplateParams = {}

    keyDelim = '-'
    termChar = ';'
    delimChar = ','

    # Constructor - Read config
    def __init__(self, configFile):
        super(TemplateKeyHandler, self).__init__(configFile)

    def getName(self):
        return 'Template'

    # Base class will call update config
    def updateConfig(self, configFile):      

        self.logDebug('Updating template config')

        with open(configFile) as jsonConfig:
            data = json.load(jsonConfig)

        configTemplates = data['templates']

        for template in configTemplates:

            self.logDebug('Template: ' + template)

            templateString = configTemplates[template]

            validParams, paramTotal = self.calculateNumParams(configTemplates[template])

            if not validParams:               
                print 'Error. Invalid template parameters in "{}"'.format(templateString)
                continue

            self.templates[template] = configTemplates[template]
            self.numTemplateParams[template] = paramTotal

            self.logDebug('Template: {}, Number of params: {}'.format(self.templates[template], self.numTemplateParams[template]))

    # Returns:
    # 1. Boolean indicating success
    # 2. Number of params
    #
    # NOTE: First param is specified as 0, hence the +1 at the return
    def calculateNumParams(self, templateString):

        highestValue = 0

        params = re.findall('\%\d\%', templateString)

        for param in params:
            self.logDebug('Calculation param: {}'.format(param))
            paramIndex = param.replace('%','')

            isInt, value = tryCastToInt(paramIndex)
            if not isInt:
                return False, 0

            if value > highestValue:
                highestValue = value

        return True, highestValue + 1

    # Substitute placeholders with supplied parameters

    def substituteParams(self, templateString, params):

        result = templateString

        for i in range(len(params)):

            previous = result

            placeholder = '%{}%'.format(i)
            result = result.replace(placeholder, params[i])

            self.logDebug('Placeholder: {}, Parameter: {}, Before: {}, After: {}'.format(placeholder, params[i], previous, result))

        return result

    # Return text match if any exists
    def getTextReplacement(self, character):

        if (self.debug):
            print 'currentKeyString: ' + self.currentKeyString
      
        # Iterate 
        for template in self.templates:  

            test1 = self.currentKeyString
            test2 = template + '-'

            # print '`%s` == `%s` ? %s', (test1, test2, test1 == test2)

            keyString = template + self.keyDelim

            pos = self.currentKeyString.find(keyString)
            if pos >= 0:

                self.logDebug('Match: First')

                paramString = self.currentKeyString[pos + len(keyString):]
                termPos = paramString.find(self.termChar)

                if (termPos > 0):
                    self.logDebug('Param string: '.format(paramString))
                    params = paramString[:termPos].split(self.delimChar)

                    self.logDebug('Match: First, Term - ' + paramString)

                    numReceivedParams = len(params)
                    numExpectedParams = self.numTemplateParams[template]
                    
                    if numExpectedParams != numReceivedParams:
                        print 'Error. Expected {} parameters but received {}'.format(numExpectedParams, numReceivedParams)
                        continue

                    templateString = self.templates[template]
                    return True, TextReplacement(len(keyString) + len(paramString), self.substituteParams(templateString, params))   

        return False, None

    