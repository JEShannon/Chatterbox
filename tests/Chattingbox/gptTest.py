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
    """
    Check that the provided agent's key management system is working properly.

    This tests the following functions:
    getKey()
    setKey()
    useKey()
    initialize()*
    *This function only ensures that initialization works in relation to the key management system.

    This test only requires a valid key if there is some sort of validation, which isn't the case at the time of writing.
    
    """
    #Check if there is currently a key there (we assume there is)
    if not gptAgent.getKey():
        print("System failed to return an initial key, ensure it has one when keyTest is called!")
        return False
    #Check if we can add a new key in
    if not gptAgent.setKey("abcd", "keyTest1"):
        print("Failed to set keyTest1 in keyTest")
        return False
    if not gptAgent.getKey("keyTest1") == "abcd":
        print("Failed to recall keyTest1 in keyTest")
        return False
    #Save the old (real) key
    realKey = gptAgent.getKey()
    #Set a new default key
    if not gptAgent.setKey("qwerty", "default"):
        print("Failed to set a new default key in keyTest")
        return False
    #Check that the default key was updated
    if not gptAgent.getKey("default") == "qwerty":
        print("Failed to recall keyTest1 in keyTest")
        return False
    #Create a new key to use under a non-default name
    if not gptAgent.setKey("bcde", "keyTest2"):
        print("Failed to set keyTest2 in keyTest")
        return False
    if not gptAgent.getKey("keyTest2") == "bcde":
        print("Failed to recall keyTest2 in keyTest")
        return False
    #Set that to be the used key
    if not gptAgent.useKey("keyTest2"):
        print("Failed to set keyTest2 to active key in keyTest")
        return False
    #Ensure we get that same key from both asking by name and by active key
    if not (gptAgent.getKey() == "bcde" and gptAgent.getKey("keyTest2") == "bcde"):
        print("Failed ensuring keyTest2 was correct from both methods of asking in keyTest")
        return False
    #Put a new key in the same non-default name
    if not gptAgent.setKey("xyz", "keyTest2"):
        print("Failed to overwrite keyTest2 in keyTest")
        return False
    #Ensure it is now found when asking by name or for the active key
    if not (gptAgent.getKey() == "xyz" and gptAgent.getKey("keyTest2") == "xyz"):
        print("Failed ensuring keyTest2 was correct the second time from both methods of asking in keyTest")
        return False
    #Create a final new key, and set it to be active on creation
    if not gptAgent.setKey("def", "keyTest3", useKey=True):
        print("Failed to create keyTest3 in keyTest")
        return False
    #Ensure it is now found when asking by name or for the active key
    if not (gptAgent.getKey() == "def" and gptAgent.getKey("keyTest3") == "def"):
        print(gptAgent.getKey(), gptAgent.getKey("keyTest3"))
        print("Failed ensuring keyTest3 was correct from both methods of asking in keyTest")
        return False
    #Replace the previous key using set key, setting it to be the default key
    if not gptAgent.setKey("foobar", "keyTest2", useKey=True):
        print("Failed to overwrite keyTest2 and set it as the default key in keyTest")
        return False
    #Ensure it is now found when asking by name or for the active key
    if not (gptAgent.getKey() == "foobar" and gptAgent.getKey("keyTest2") == "foobar"):
        print("Failed ensuring keyTest2 was correct the third time from both methods of asking in keyTest")
        return False
    #Set the default key to the original key
    if not gptAgent.setKey(realKey, "real", useKey=True):
        print("Failed to reintroduce the real key and set it as the default key in keyTest")
        return False
    #Ensure it initializes properly
    if not gptAgent.initialize(noContext=True):
        print("Failed to initialize in keyTest")
        return False
    return True

def transcriptTest(gptAgent):
    """
    Check the agent's transcript management system to ensure it works properly.

    This test set tests the following functions:
    GptBox.setContext()*
    GptBox.initialize()*
    GptBox.makeContextValid()
    GptBox.prompt()
    GptBox.getTranscript()
    GptBox.setTranscript()
    GptBox.respond()

    *setContext and initialization is only tested to ensure a use case beginning at an empty starting context to eventual initialization
      functions correctly, as this was a discovered bug during development.
    """
    #First set the context to a single line to ensure a consistent start
    transcript = []
    startingContext = gptAgent.makeContextValid("This is a debugging test you are helping with.  Answer shortly and accurately.", 0)
    gptAgent.setContext(startingContext)
    transcript.append(startingContext)
    #Now initialize, assume there was a valid key
    if not gptAgent.initialize():
        print("Failed to initialize in transcriptTest.")
        return False
    #Ensure the transcript is correct
    if not __compareContexts(gptAgent.getTranscript(), transcript):
        print("Failed initial check in transcriptTest.")
        return False
    #Add to the transcript, using each type of operator using individual calls
    scripts = [gptAgent.makeContextValid("System message!", 0),
               gptAgent.makeContextValid("User message!", 1),
               gptAgent.makeContextValid("Agent message!", 2)]
    for script in scripts:
        gptAgent.prompt(script)
        transcript.append(script)
    #Validate it
    if not __compareContexts(gptAgent.getTranscript(), transcript):
        print("Failed multiple update calls test in transcriptTest.")
        return False
    #Add to the transcript, using each type of operator in a list with a single call
    scripts = [gptAgent.makeContextValid("Second system message!", 0),
               gptAgent.makeContextValid("Second user message!", 1),
               gptAgent.makeContextValid("Second agent message!", 2)]
    gptAgent.prompt(scripts)
    transcript.extend(scripts)
    #Validate it
    if not __compareContexts(gptAgent.getTranscript(), transcript):
        print("Failed single update call test in transcriptTest.")
        return False
    #Replace the transcript
    finalScript = [startingContext,
                   gptAgent.makeContextValid("What is your name?", 2)]
    gptAgent.updateTranscript(finalScript)
    transcript = []
    transcript.extend(finalScript)
    #Validate it
    if not __compareContexts(gptAgent.getTranscript(), transcript):
        print("Failed transcript replacement call test in transcriptTest.")
        return False
    #Get a response from the agent
    agentResponse = gptAgent.makeContextValid(gptAgent.respond().content, 2)
    transcript.append(agentResponse)
    #Ensure that the response was saved properly
    if not __compareContexts(gptAgent.getTranscript(), transcript):
        print("Failed response recording test in transcriptTest.")
        return False
    return True
