import sys

def __compareContexts(con1, con2):
    if not (isinstance(con1, list) and isinstance(con2, list)):
        return False
    if not len(con1) == len(con2):
        return False
    for i in range(len(con1)):
        if not con1[i] == con2[i]:
            return False
    return True


def contextTest(gptAgent):
    """
    Test the context features of GPTChatter to ensure they work correctly.

    This tests the following functions:
    GptBox.getContext()
    GptBox.makeContextValid()
    GptBox.addContext()
    GptBox.setCintext()
    GptBox.initialize()*
    GptBox.getTranscript()*
    *This function only ensures that initialization and the transcript is correct in relation to the context.

    In order to work, this agent must already have a valid key, or the initialization test will fail.

    """
    #First get the current context
    expContext = gptAgent.getContext()
    #Then add a line to the context as the user
    newCon = gptAgent.makeContextValid("Hi!", 1)
    gptAgent.addContext(newCon)
    expContext.append(newCon)
    #Ensure the context was added correctly
    if not __compareContexts(expContext, gptAgent.getContext()):
        print("Adding user context failed to be consistent!")
        return False
    #Add context using the AI's operator
    newCon = gptAgent.makeContextValid("ai operator", 2)
    gptAgent.addContext(newCon)
    expContext.append(newCon)
    #Ensure the context is correct again
    if not __compareContexts(expContext, gptAgent.getContext()):
        print("Adding agent context failed to be consistent!")
        return False
    #Replace the context, with all three tags of context used
    expContext = []
    newCon = []
    sysCon = gptAgent.makeContextValid("system context", 0)
    userCon = gptAgent.makeContextValid("user context", 1)
    aiCon = gptAgent.makeContextValid("ai context", 2)
    newCon.append(sysCon)
    newCon.append(userCon)
    newCon.append(aiCon)
    gptAgent.setContext(newCon)
    expContext.extend(newCon)
    #Fetch the context, ensure it is correct again
    if not __compareContexts(expContext, gptAgent.getContext()):
        print("Replacing the context failed to be consistent!")
        return False
    #Initialize the agent and ensure no problems
    if not gptAgent.initialize():
        print("Failed to initialize after replacing the context!")
        return False
    #Now ensure the transcript is the same as the original context!
    if not __compareContexts(expContext, gptAgent.getTranscript()):
        print("The expected transcript post-initialization failed to be consistent!")
        return False
    return True

def keyTest(gptAgent):
    #Check if there is currently a key there (we assume there is)
    #Check if we can add a new key in
    #Save the old (real) key
    #Set a new default key
    #Check that the default key was updated
    #Create a new key to use under a non-default name
    #Set that to be the used key
    #Ensure we get that same key from both asking by name and by active key
    #Put a new key in the same non-default name
    #Ensure it is now found when asking by name or for the active key
    #Set the default key to the original key
    #Ensure it initializes properly
    pass
