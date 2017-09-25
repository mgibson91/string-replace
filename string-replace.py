import sys
sys.path.append('pyperclip-1.5.27')

import pyperclip

import pyxhook

import subprocess
import json


logFileName       ='/tmp/keys-history.log'
delimiter      = '-'
currentString  = ''
aliases        = {}


def getReplacements(configFile):

    with open(configFile) as data_file:    
        data = json.load(data_file)

    if 'aliases' not in data:
        return 'No config file found.', {}

    aliasReplacements = data['aliases']

    values = {}

    for alias in aliasReplacements:
        values[alias] = aliasReplacements[alias]

    return '', values


# Returns:
# - Boolean determining whether a replacement match was found
# - Replacement string
def checkForReplacement(alias):

  if (alias in aliases):
    return True, aliases[alias]

  return False, ''

# Using 'BackSpace' remove the required number of characters
def removeCharacters(numChars):

  for i in range(numChars):
    subprocess.check_output('/usr/bin/xdotool key BackSpace', shell=True)
    
# Paste replacement string
def pasteReplacement(replacement):

  windowName = subprocess.check_output('xdotool getwindowname $(xdotool getwindowfocus)', shell=True)

  # Window name containing '@' is most likely a terminal. SSH session terminals don't return a window name
  if '@' in windowName or len(windowName) == 0:
    subprocess.check_output("echo \"" + replacement + "\" > /tmp/temp-string-replace",  shell=True)
    subprocess.check_output("xsel --input < /tmp/temp-string-replace",                  shell=True)

  # Use pyperclip for GUI applications
  else:
    pyperclip.copy(replacement)

  subprocess.check_output('/usr/bin/xdotool key --clearmodifiers Shift+Insert', shell=True)

def replaceString(alias, replacement):

  # Remove alias. Bear in mind we need to add 2 characters to the remove length to account for the two already stripped '-' characters
  removeCharacters(len(alias) + 2)
  pasteReplacement(replacement)


def log(message, file):

  if (file):
    file.write(message)

# This function is called everytime a key is pressed.
def OnKeyPress(event):

  global currentString

  currentChar = chr(event.Ascii)
  isDelimiter = (currentChar == delimiter)

  logFile=open(logFileName,'a')

  # If we already have an alias or this character is a delimiter, add to currentString
  if (delimiter in currentString) or isDelimiter:

    currentString += currentChar

    # If string is at least 3 characters, check to see if a 
    if len(currentString) > 1 and isDelimiter:

      log('Two delimiters found, checking for match\n', logFile)

      # Remove last and first delimiter chars
      alias = currentString[:-1][1:]
      found, replacement = checkForReplacement(alias)

      if (found):
        log('Replacement found\n', logFile)
        replaceString(alias, replacement)
      else:
        log('No replacement found\n', logFile)
      
      # Reset current alias
      currentString = ''

  if len(currentString) > 0:
    log('Current alias: {}\n'.format(currentString), logFile)

  if currentChar=='q':
    logFile.close()
    new_hook.cancel()


##### ENTRY POINT #####

# Get aliases and replacements from config file
errorMsg, aliases = getReplacements('config.json')

if errorMsg:
  print ('Error reading config file. Exiting. {}'.format(errorMsg))


new_hook=pyxhook.HookManager()  # Instantiate HookManager class
new_hook.KeyDown=OnKeyPress     # Listen to all keystrokes
new_hook.HookKeyboard()         # Hook the keyboard
new_hook.start()                # Start the session
