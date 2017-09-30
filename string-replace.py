import sys
import subprocess
import json
import shlex
import os.path

import pyxhook
sys.path.append('pyperclip-1.5.27')
import pyperclip

from key_handlers.handler_base import BaseKeyHandler, TextReplacement
from key_handlers.handler_alias import AliasKeyHandler

debug       = False
logFileName = '/tmp/keys-history.log'

textHandlers = []

exitCount = 0

def getConfigFile():

    userConfigFile    = './config.json'
    defaultConfigFile = './config.json.default'

    configFile = ''

    if os.path.isfile(userConfigFile):
        configFile = userConfigFile

    elif os.path.isfile(defaultConfigFile):
        configFile = defaultConfigFile

    return configFile        

#
# Using 'BackSpace' remove the required number of characters
def removeCharacters(numChars):

    for _ in range(numChars):
        subprocess.check_output('/usr/bin/xdotool key BackSpace', shell=True)

# Paste replacement string
def pasteReplacement(replacement, isTerminal):

    if isTerminal:
        subprocess.check_output(
            "echo \"" + replacement + "\" > /tmp/temp-string-replace",  shell=True)
        subprocess.check_output(
            "xsel --input < /tmp/temp-string-replace",                  shell=True)

    # Use pyperclip for GUI applications
    else:
        pyperclip.copy(replacement)

    subprocess.check_output(
        '/usr/bin/xdotool key --clearmodifiers Shift+Insert', shell=True)


def replaceString(removeLength, replacement, isTerminal):

    removeCharacters(removeLength)
    pasteReplacement(replacement, isTerminal)

# def log(message, logFile):
#     if (logFile):
#         logFile.write(message)

def resetTextHandlers():
    
    for handler in textHandlers:        
        if handler:
            handler.reset()

# This function is called everytime a key is pressed.
def OnKeyPress(event):

    global currentString
    global exitCount

    # logFile = open(logFileName, 'a')

    for handler in textHandlers:

        isMatch, replacement = handler.getTextReplacement(event)

        if isMatch:
            
            isTerminal = 'term' in event.WindowProcName
            replaceString(replacement.removeLength, replacement.text, isTerminal)

            # Reset all handlers and return
            resetTextHandlers()
            return


    if chr(event.Ascii) == '`':
        exitCount += 1

        if exitCount > 1:
            # logFile.close()
            new_hook.cancel()
    else:
        exitCount = 0


# Get config data
configFile = getConfigFile()

if not configFile :
    print 'No config files found. Exiting'
    exit(1)

# Add key handlers

# Alias key handler
try:
    textHandlers.append(AliasKeyHandler(configFile))
except Exception as e:
    print 'Unable to add alias key handler: {}'.format(e)

new_hook = pyxhook.HookManager()  # Instantiate HookManager class
new_hook.KeyDown = OnKeyPress     # Listen to all keystrokes
new_hook.HookKeyboard()           # Hook the keyboard
new_hook.start()                  # Start the session
