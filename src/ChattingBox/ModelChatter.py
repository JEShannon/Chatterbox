#This model is to hold the main class that all chatterboxes use.

DEFAULT_KEY_NAME = "default"

class chatterbox ():
    #Functions for setting the context for the bot and initialization
    def checkForKeys(self):
        """Check for an .apikeys file containing openai keys"""
        keyNames = []
        with open(self.__keyLoc) as keyFile:
            for keyLine in keyFile:
                if(not keyLine.strip()):
                    continue
                #check if the line even exists!
                #TODO: See if you can validate the key somehow, right now it just trusts it.
                #TODO: Use OS environ vars to load default keys
                name = DEFAULT_KEY_NAME
                keyTokens = keyLine.strip().split(":")
                if(len(keyTokens) > 2):
                    print("More than two tokens found on a line in the keys file, skipping...", file=sys.stderr)
                    continue
                if(len(keyTokens) == 2 and keyTokens[0].strip()):
                    #this one has a name, use it!
                    name = keyTokens[0].strip()
                if(keyTokens[-1].strip()):
                    keyNames.append(name)
                    self.__keys[name] = keyTokens[-1]
        if(not self.__keys):
            print("Warning, no keys found.  Ensure keys are set before using!", file=sys.stderr)
        else:
            #set ourselves to the key default if it exists, otherwise whichever was first
            if DEFAULT_KEY_NAME in keyNames:
                self.__activeKey = DEFAULT_KEY_NAME
            else:
                self.__activeKey = keyNames[0]
    
    def __init__(self, context="", keyLoc="", key=None, keyName=None, saveKeys=True):
        self.__context = context
        self.__keyLoc = keyLoc
        self.__saveKeys = saveKeys
        if key:
            if keyName:
                self.setKey(key, keyName, useKey=True)
            else:
                self.setKey(key, DEFAULT_KEY_NAME, useKey=True)
        else:
            self.checkForKeys()
    
    def addContext(self, newContext):
        if isinstance(newContext, str):
            self.__context.append(newContext)
            return True    
        if isinstance(newContext, list):
            self.__context.extend(newContext)
            return True
        return False

    def setContext(self, newContext):
        if isinstance(newContext, str):
            self.__context = [newContext]
            return True
        if isinstance(newContext, list):
            self.__context = newContext
            return True
        return False

    def getContext(self):
        return self.__context

    def setKey(self, key, keyName, *, useKey):
        pass

    def getKey(self, keyName):
        pass

    def useKey(self, keyName):
        pass

    def initialize(self):
        pass

    def isInitialized(self):
        pass

    #Functions for interacting with the bot
    def respond(self):
        pass

    def prompt(self, text):
        pass

    def getTranscript(self):
        pass

    def updateTranscript(self):
        pass
    
