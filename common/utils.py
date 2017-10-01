def tryCastToInt(value):

    try:        
        return True, int(value)
    except ValueError:
        return False, 0

def getValueFromDictionary(dictionary, key, default):

    if dictionary and key in dictionary:
        return dictionary[key]
    else:
        return default

def getIntValueFromDictionary(dictionary, key, default):

    if dictionary and key in dictionary:
        result = dictionary[key]
        isInt, value = tryCastToInt(result)
        return value if isInt else default

    else:
        return default

def getBoolValueFromDictionary(dictionary, key, default):

    if dictionary and key in dictionary:
        return dictionary[key].lower() in ['true','yes','on','enabled']
    
    else:
        return default
