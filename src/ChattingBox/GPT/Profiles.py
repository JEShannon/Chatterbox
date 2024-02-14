
def TEXT_TO_SCRIPT(text):
    #this function takes normal sentence by sentence text and converts it to a valid script
    #it is intended that any script returned by this function will pass validateContext()
    #this will not return anything if the text input is not a string or a list of strings
    if (not isinstance(text, str)) and (not isinstance(text, list)):
        return None
    result = []
    lines = text
    if isinstance(text, str):
        lines = [text]
    for line in lines:
        result.append('system:'+line)
    return result

class AgentProfile:
    def __init__(self, name, desc, script):
        self.name = name
        self.desc = desc
        self.__script = script

    def getScript(self):
        return self.__script.copy()


_SecondOpinionScript =  ["You are a helper trying to give positive but generic advice to a human who is confused about what to do.",
                         "You don't know this human personally and also don't know what their problems are before hand but will still try your best.",
                         "Assume that each problem the user has are related unless the user says otherwise, and if you don't know how to help you will say that.",
                         "Any attempts to steer the conversation away from giving advice should be stopped by you before they get too far away from the point of the conversation.",
                         "Finally, you must note before any advice that you are just offering suggestions.",
                         ]

 