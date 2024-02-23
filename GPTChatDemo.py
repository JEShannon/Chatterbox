from src.ChattingBox.GPTChatter import *


#Just give it a singular test, see if it can respond correctly when asked to perform a simple task.

myPrompt = ["system : Please respond by only writing one line containing only the name of the company that owns google."]

#####
#
# NOTE: This requires an API key to run properly!
#       Add one in src/ChattingBox/GPT/openAI.apikeys
#       (You will need to make that file)
#       It will work if it is the only text in the file.
#
#####

def main():

    box = GptBox(context=myPrompt)

    box.initialize()

    response = box.respond()

    print("What is the company that owns Google?")

    #print(response)
    print(response.content)

    if not response:
        print("Error!  Unable to get input from the model.  Ensure it is working correctly and has a proper connection to needed servers.", file=sys.stderr)
        return

    strResponse = str(response.content)

    
    if not strResponse.strip()[:8].casefold() == "Alphabet".casefold():
        print("response was not entirely as expected, have a human inspect the prompt!")
    else:
        print("ChatGPT got the question right!")

if __name__ == "__main__":
    main()
