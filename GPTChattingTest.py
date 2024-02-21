import src.ChattingBox.GPTChatter as gptchat
import src.ChattingBox.GPT.Profiles as gptprof

#Bring in the main class, and try to run it, to ensure everything is working properly

profile = gptprof.Advisor
agent = gptchat.GptBox(context=profile.getScript())
agent.initialize()
#Just ask it a simple question to start
agent.prompt(gptchat.USEROPERATOR + ": Can you help me with some homework?")
agent.respond()
for line in agent.getTranscript():
    print(line)
