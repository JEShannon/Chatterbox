import openai
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
    if singleLine:
        return __validateLine(context)
    #multi-line contexts must both be lists of strings, and have every line validate correctly.
    if not isinstance(context, list):
        return False
    for line in context:
        if not __validateLine(line):
            return False
    return True

class GptBox(chatterbox):
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
        if(context and validateContext(context)):
            self.context = context
        elif(context):
            raise Exception("Context must be a list of strings.  See formatting guidelines for acceptable examples.")
        
