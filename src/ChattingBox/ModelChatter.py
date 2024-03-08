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
        self.__context = [context] if isinstance(context, str) else context
        self.__keyLoc = keyLoc
        self.__saveKeys = saveKeys
        self.__keys = {}
        self.__keysUpdated = False
        if key:
            if keyName:
                self.setKey(key, keyName, True)
            else:
                self.setKey(key, DEFAULT_KEY_NAME, True)
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

    def setKey(self, key, keyName, useKey=False):
        """
        Save a key to the manager under a specified name, if both exist

        Keyword Arguements:
        key - Object representation of the key, must exist
        keyName - String name for the key, must exist and be a string
        useKey [specified only] - if true, set this to be the key used by the agent
        """
        if (not key) or (not keyName) or (not isinstance(keyName, str)):
            return False
        self.__keys[keyName] = key
        self.__keysUpdated = True
        if(useKey):
            self.__activeKey = keyName
        return True

    def getKey(self, keyName, default=None):
        """Get the key specified.  Return default if it doesn't exist."""
        #if no name is supplied, get the key we are currently using
        if not keyName:
            return self.__keys.get(self.__activeKey, default)
        return self.__keys.get(keyName, default)

    def useKey(self, keyName):
        #TODO: validate the key somehow, but currently it just accepts it if it exists at all
        #Returns true if the system successfully swapped to the key
        #Returns false if the key wasn't found
        #Note that a key MUST be set in order to fully initialize
        if self.__keys.get(keyName):
            self.__activeKey = keyName
            return True
        return False

    def getCurrentKeyName(self):
        """Get the name of the key we are using."""
        return self.__activeKey

    def initialize(self, key=None, context=None, noContext=False):
        """Check if the object is able to be initialized.

        Return the key if True, otherwise return None."""
        #check if context was passed to the function, and after adding it check that the context exists
        if(context and not noContext):
            self.setContext(context)
        if (not self.__context) and (not noContext):
            print("Warning!  No context for agent!  Aborting!", file=sys.stderr)
            return None
        self.__transcript = self.__context
        #check that there is an active key selected.
        if key:
            #everything is correct, return the key
            #if the key was given here, we aren't saving it
            return key
        else:
            if not self.getKey():
                print("No keys were found!  Either give one to the initialize function or set it with setKey!", file=sys.stderr)
            return self.getKey()
            

    def isInitialized(self):
        """Subclasses must determine if initialization is done.

        This always returns false"""
        return False

    #Functions for interacting with the agent
    def respond(self):
        pass #This is always subclass specific

    def prompt(self, text):
        if isinstance(text, str):
            self.__transcript.append(text)
        else:
            self.__transcript.extend(text)

    def getTranscript(self):
        return self.__transcript

    def updateTranscript(self, script):
        if isinstance(script, str):
            self.__transcript = [script]
        else:
            self.__transcript = script
    
