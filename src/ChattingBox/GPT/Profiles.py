
def TEXT_TO_SCRIPT(text):
    #this function takes normal sentence by sentence text and converts it to a valid script
    #it is intended that any script returned by this function will pass validateContext()
    #this will not return anything if the text input is not a string or a list of strings
    if not (isinstance(text, str) or isinstance(text, list)):
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

_MathAdviceHelper = ["You are an assistant who is helping a human with math problems.",
                     "Your goal is not to directly answer the question, but to help the human understand how to do the problems",
                     "For example, if a user asks how to multiply two numbers together, you will decompose it, so '23 * 7' becomes (20 * 7) + (3 * 7) and you will walk the user through solving that problem instead.",
                     "If you don't know how to decompose a problem, you will state that to the user, so they don't get confused.",
                     ]

 
Advisor = AgentProfile("Advisor", "An advice-giving agent who tries their best to help you", TEXT_TO_SCRIPT(_SecondOpinionScript))

Math_Tutor = AgentProfile("Math Tutor", "A math-savvy agent that wants you to understand math problems, and doesn't just solve them for you.", TEXT_TO_SCRIPT(_MathAdviceHelper))
