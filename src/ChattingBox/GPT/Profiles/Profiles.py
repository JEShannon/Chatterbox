
class AgentProfile:
    def __init__(self, name, desc, script):
        self.name = name
        self.desc = desc
        self.__script = script

    def getScript(self):
        return self.__script.copy()
