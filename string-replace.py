import sys
import subprocess
import time
import json
import shlex
import signal
import threading
import os.path

import pyxhook
sys.path.append('pyperclip-1.5.27')
import pyperclip

from key_handlers.handler_base import BaseKeyHandler, TextReplacement
from key_handlers.handler_alias import AliasKeyHandler
from key_handlers.handler_template import TemplateKeyHandler


# Register SIGINT handler to exit on 'ctrl + C'
def sigintHandler(signum, frame):
    print 'Exiting'
    keyHookManager.cancel()
    exit(0)

signal.signal(signal.SIGINT, sigintHandler)

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
        subprocess.check_output("echo \"" + replacement + "\" > /tmp/temp-string-replace",  shell=True)
        subprocess.check_output("xsel --input < /tmp/temp-string-replace",                  shell=True)

    # Use pyperclip for GUI applications
    else:
        pyperclip.copy(replacement)

    subprocess.check_output('/usr/bin/xdotool key --clearmodifiers Shift+Insert', shell=True)


def replaceString(removeLength, replacement, isTerminal):

    removeCharacters(removeLength)
    
    try:
        pasteReplacement(replacement, isTerminal)
    except Exception as e:
        print 'Got error `{}` pasting text: {}'.format(e, replacement)
    

def resetTextHandlers():
    
    for handler in textHandlers:        
        if handler:
            handler.reset()

# This function is called everytime a key is pressed.
def OnKeyPress(event):

    global currentString
    global exitCount

    for handler in textHandlers:

        isMatch, replacement = handler.checkForTextReplacement(event)
        if isMatch:
            
            isTerminal = 'term' in event.WindowProcName
            replaceString(replacement.removeLength, replacement.text, isTerminal)

            # Reset all handlers and return
            resetTextHandlers()
            return


# Get config data
configFile = getConfigFile()

if not configFile :
    print 'No config files found. Exiting'
    exit(1)

# Add key handlers
textHandlers = []


# Alias key handler
try:
    textHandlers.append(AliasKeyHandler(configFile))
except Exception as e:
    print 'Unable to add alias key handler: {}'.format(e)

# Template key handler
try:
    textHandlers.append(TemplateKeyHandler(configFile))
except Exception as e:
    print 'Unable to add template key handler: {}'.format(e)


keyHookManager = pyxhook.HookManager()  # Instantiate HookManager class
keyHookManager.KeyDown = OnKeyPress     # Listen to all keystrokes
keyHookManager.HookKeyboard()           # Hook the keyboard

def logKeys():
    keyHookManager.start()             # Start the session

keyLoggingThread = threading.Thread(target=logKeys)
keyLoggingThread.start()

while(True):
    time.sleep(1000)
