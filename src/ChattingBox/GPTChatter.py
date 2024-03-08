import openai
import os
import sys
from .ModelChatter import chatterbox
#NOTE: To run just this like a script, you must use the -m flag in your python command
#If not, there will be a relative import error!  This is needed for the module to work correctly

__validmodels = ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k", ]
__validoperators = ["system", "user", "assistant", ] #all valid operators
AIOPERATOR = __validoperators[2] #the operator for the AI specifically
USEROPERATOR = __validoperators[1]
#possible TODO: allow this to be changed somehow?  Likely unneeded

DEBUG_OUTPUT = False

DEFAULT_KEY_NAME = "default"
#files are stored in the local folder GPT, in openai.apikeys
KEYS_LOCATION = os.path.join(os.path.dirname(sys.modules[__name__].__file__), "GPT", "openAI.apikeys")

def getValidModels():
    return __validmodels

def validateModelName(name):
    return name in __validmodels

def getValidOperators():
    return __validoperators

def __validateLine(line):
    #if the line is a string, and is formatted as "[system|user|assistant]:[Message]", then it is valid!
    if(not isinstance(line, str)):
        return False
    tokens = line.split(":", 1)
    if (not (tokens[0].strip().lower() in __validoperators and tokens[1].strip())):
        return False
    return True

def validateContext(context, singleLine = False):
    """
    Validate that the context is correct and won't cause errors during API calls.
    Valid context can be either a single string or a list of strings

    Keyword Arguments:
    context - object that may be valid context for API calls
    singleLine - if true, forces the context to be a single string
    """
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
    with open(KEYS_LOCATION, 'w') as keyFile:
        keystring = keyMap.get(DEFAULT_KEY_NAME, default="")
        for key in keyMap:
            if(key == DEFAULT_KEY_NAME):
                continue
            keystring = keystring + '\n' + key + ":" + keyMap[key]
        keyFile.write(keystring)

class GptBox(chatterbox):
    """
    This class wraps around the openai API to handle busywork like key and transcript management.
    
    In order to function correctly, the object must be properly initialized after creation, through the initialize() method.
    This module also requires a key (either given or from a file) in order to be initialized.
    If initialized, the object should have all the information needed to call the API, provided it is accurate.

    Public methods:
    addContext - adds to the existing context for the agent
    setContext - replaces the existing context for the agent
    getContext - returns the initial context used for the agent
    setKey - sets a key that instances of this agent can use
    getKey - gets a key known to this class
    getCurrentKeyName - get the identifier for the key currently chosen for use
    useKey - choose a key to use for agents that is already known to this class
    initialize - create an instance for a new agent ready to use the API
    isInitialized - check if an object is initialized
    respond - call the API and record the response
    prompt - add (typically human) input for the agent to consider
    getTranscript - get a copy of the transcript with the agent
    updateTranscript - replace the transcript with the agent
    """

    def checkForKeys(self):
        super().checkForKeys()
        
    def __init__(self, *, model_type = "gpt-3.5-turbo", context = "", key=None, keyName=None, saveKeys=True):
        """
        Create the object, and populate the fields given by the user.
        The defaults here ensure that the system can run provided a valid API kay already exists in the openAI.apikeys file

        Keyword Arguments:
        model_type - Which model to use, currently only a few models are accepted, though the naming is somewhat lenient for gpt4/gpt3.5
        context - Context that should be validated first, but otherwise is used as the base instructions for the model
        key - The specific key to use for the model.  Currently there is no key validation.  This key will be saved unless specified otherwise
        keyName - The indentifier for this key.  This must be a string, and if not specified or invalid "default" will be used
        saveKeys - Whether the keys should be saved or not.  If set to false, the system will not save any keys passed to it to disk
        """
        if(not validateModelName(model_type)):
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
        self.__aiModel = model_type
        #now initialize the settings so we can add context if present
        if(context and not validateContext(context)) or ((not context) and (not context == "")):
            raise Exception("Context must be a list of strings.  See formatting guidelines for acceptable examples.")
        super().__init__(context, KEYS_LOCATION, key, keyName, saveKeys)
        self.__apiClient = None
        self.__initialized = False

    def makeContextValid(self, context, operator = None):
        op = None
        #If the operator is a number and < len of validoperators, use it
        if isinstance(operator, int) and operator < 3 and operator >= 0:
            op = getValidOperators()[operator]
        #If the operator is a word used in validoperators use it
        if operator in getValidOperators():
            op = operator
        #otherwise print an error and return the original object
        if not op:
            print("Error, the operator",operator,"is not valid!  Use GPTChatter.getValidOperators() for a full list!", file=sys.stderr)
            return context
        #now simply add the tag for the user operator for each line and return
        if isinstance(context, str):
            return op + ":" + context
        elif isinstance(context, list):
            con = []
            for line in context:
                if not isinstance(context, list):
                    print("Error, the context must be a string or list of strings, instead found type", type(line), "in the list.", file=sys.stderr)
                    return context
                con.append(op + ":" + line)
            return con
        print("Error, the context must be a string or list of strings, instead found type", type(line), file=sys.stderr)
        return context

    def addContext(self, newContext):
        """Add the given context to the existing context the model has, if it is valid."""
        if validateContext(newContext):
            return super().addContext(newContext)

    def setContext(self, newContext):
        """Replace the context with the given context, if it is valid."""
        #returns true if the context was accepted, false otherwise
        if validateContext(newContext):
            return super().setContext(newContext)
        return False

    def getContext(self):
        """Return the context."""
        return super().getContext()

    #TODO: use the environment variables to hold default keys
    def setKey(self, key, keyName, *, useKey=False):
        return super().setKey(key, keyName, useKey)

    def getKey(self, keyName=None, *, default=None):
        return super().getKey(keyName, default)

    def getCurrentKeyName(self):
        return super().getCurrentKeyName()

    def useKey(self, keyName):
        """Change the key we are using to the specified one, if it exists."""
        return super().useKey(keyName)

    def initialize(self, *, key=None, context=None, noContext=False):
        """
        Ensure that all needed parameters for using the API are ready.
        If they are, allow the object to start interacting with the API.
        All function params are optional and must be specified.

        Keyword Arguements:
        key - A key to be used for accessing the OpenAI API
        context - Agent context to inform the agent's responses.  Must be valid
        noContext - If true, the agent ignores any checks for context and starts with no context at all.
        """
        #first check if the context exists or if the user provided context here
        if context and not self.validateContext(context):
            print("Warning!  Given context is invalid!  Aborting!", file=sys.stderr)
            return False
        key = super().initialize(key, context, noContext)
        ##### TODO FINISH INITIALIZATION
        #Everything is now ready to begin, so wrap up and return
        self.__apiClient = openai.OpenAI(api_key = key)
        self.__initialized = True
        return True

    def isInitialized(self):
        """Check if the object has finished initialization."""
        return self.__initialized

    def __transcriptToAPI(self):
        #take the transcript, and turn it into a form usable by the API
        #the API expects a list of dicts, each having a "role" and "content" key
        apiDictList = []
        for line in super().getTranscript():
            parts = line.split(":")
            apiDict = {"role":parts[0].strip(), "content":parts[1].strip()}
            if DEBUG_OUTPUT:
                print(apiDict)
            apiDictList.append(apiDict)
        return apiDictList

    def __APIToTranscript(self, response):
        #given the following response, add it to the transcript
        newResponse = self.makeContextValid(str(response), AIOPERATOR)
        return self.prompt(newResponse)

    def respond(self):
        """Call the API and get the LLM's response.  Save it and return the response."""
        if not self.__initialized:
            print("Error, not initialized, use initialize() first!", file=sys.stderr)
            return None
        #get a response via the API
        response = self.__apiClient.chat.completions.create(
                model=self.__aiModel,
                messages = self.__transcriptToAPI()
                ).choices[0].message
        #add the response to the transcript
        self.__APIToTranscript(response.content)
        #return the response
        return response

    def prompt(self, text):
        """Add text to the transcript to help guide the agent."""
        if not self.__initialized:
            print("Error, not initialized, use initialize() first!", file=sys.stderr)
        if not validateContext(text):
            return False
        super().prompt(text)
        return True

    def getTranscript(self):
        """Get the current trascript."""
        if not self.__initialized:
            print("Error, transcript is made during initialization, use initialize() first!", file=sys.stderr)
            return None
        return super().getTranscript()
    

    def updateTranscript(self, newTranscript):
        """Replace the transcript, if it is valid."""
        if not self.__initialized:
            print("Error, the transcript value is made during initialization, use initialize() first!", file=sys.stderr)
            return False
        if validateContext(newTranscript):
            super().updateTranscript(newTranscript)
            return True
        return False

