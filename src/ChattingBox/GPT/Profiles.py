
def TEXT_TO_SCRIPT(text):
    #this function takes normal sentence by sentence text and converts it to a valid script
    #it is intended that any script returned by this function will pass validateContext()
    pass

class AgentProfile:
    def __init__(self, name, desc, script):
        self.name = name
        self.desc = desc
        self.__script = script

    def getScript(self):
        return self.__script.copy()


_SecondOpinionScript = 

