import openai
import os
import sys
from ModelChatter import chatterbox

__validmodels = ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k", ]
__validoperators = ["system", "user", "assistant", ]

def getValidModels():
    return __validmodels

def getValidOperators():
    return __validoperators

def __validateLine(line):
    #if the line is a string, and is formatted as "[system|user|assistant]: [Message]", then it is valid!
    if(not isinstance(line, str)):
        return False
    tokens = line.split(":", 1)
    if (not (tokens[0].strip().lower() in __validoperators and tokens[1].strip())):
        return False
    return True

def validateContext(context, singleLine = False):
    #this function ensures that the context given is valid
    if singleLine or isinstance(context, str):
        return __validateLine(context)
    #multi-line contexts must both be lists of strings, and have every line validate correctly.
    if not isinstance(context, list):
        return False
    for line in context:
        if not __validateLine(line):
            return False
    return True

def __saveKeys(keyMap):
    if not keyMap:
        return
    keysLoc = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "GPT", "openAI.apikeys")
    with open(keysLoc, 'w') as keyFile:
        keystring = keyMap.get("default", default="")
        for key in keyMap:
            if(key == "default"):
                continue
            keystring = keystring + '\n' + key + ":" + keyMap[key]
        keyFile.write(keystring)

class GptBox(chatterbox):
    def __checkForKey(self):
        #files are stored in the local folder GPT, in openai.apikeys
        keysLoc = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "GPT", "openAI.apikeys")
        with open(keysLoc) as keyFile:
            for keyLine in keyFile:
                if(not keyLine.strip()):
                    continue
                #check if the line even exists!
                #TODO: See if you can validate the key somehow, right now it just trusts it.
                #TODO: Use OS environ vars to load default keys
                name = "default"
                keyTokens = keyLine.strip().split(":")
                if(len(keyTokens) > 2):
                    print("More than two tokens found on a line in the keys file, skipping...", file=sys.stderr)
                    continue
                if(len(keyTokens) == 2 and keyTokens[0].strip()):
                    #this one has a name, use it!
                    name = keyTokens[0].strip()
                if(keyTokens[-1].strip()):
                    self.__keys[name] = keyTokens[-1]
        if(not self.__keys):
            print("Warning, no keys found.  Ensure keys are set before using!", file=sys.stderr)
        
    def __init__(self, *, model_type = "gpt-3.5-turbo", context = ""):
        if(not model_type in __validmodels):
            #check if the user wrote something like "gpt4"
            if(model_type.lower() == "gpt4"):
                model_type = "gpt-4"
            elif(model_type.lower == "gpt3" or
                 model_type.lower == "gpt-3" or
                 model_type.lower == "gpt3.5" or
                 model_type.lower == "gpt-3.5"):
                model_type = "gpt-3.5-turbo"
            else:
                #throw an error and return, don't try to keep going
                raise Exception("Invalid model name, use getValidModels to see valid options.")
                return
        #now initialize the settings so we can add context if present
        self.__context = []
        if(context and validateContext(context)):
            self.__context = context
        elif(context):
            raise Exception("Context must be a list of strings.  See formatting guidelines for acceptable examples.")
        self.__keys = {}
        self.__checkForKey()
        self.__activeKey = None
        self.__initialized = False

    def addContext(self, newContext):
        if validateContext(newContext):
            if isinstance(newContext, str):
                self.__context.append(newContext)
            else:
                self.__context.extend(newContext)

    def setContext(self, newContext):
        if validateContext(newContext):
            if isinstance(newContext, str):
                self.__context = [newContext]
            else:
                self.__context = newContext

    def getContext(self):
        return self.__context

    #TODO: use the environment variables to hold default keys
    def setKey(self, key, keyName):
        return self.__keys[keyName] = key

    def getKey(self, keyName=None, *, default=None):
        #if no name is supplied, get the key we are currently using
        if not keyName:
            return self.__keys.get(self.__activeKey, default=default)
        return self.__keys.get(keyName, default=default)

    def useKey(self, keyName):
        #TODO: validate the key somehow, but currently it just accepts it if it exists at all
        #Returns true if the system successfully swapped to the key
        #Returns false if the key wasn't found
        #Note that a key MUST be set in order to fully initialize
        if self.__keys.get(keyName):
            self.__activeKey = keyName
            return True
        return False

    def initialize(self):
        pass

    def isInitialized(self):
        return self.__initialized
