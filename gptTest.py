import sys

from .GPTChatter import *


#Just give it a singulat test, see if it can respond correctly when asked to perform a simple task.

myPrompt = ["system : Please respond by only writing the following three letters in the NATO Phonetic Alphabet: A B C"]

#A correct response is first any response, and then secondly the text should read "Alpha Bravo Charlie"

def main():

    box = GptBox(context=myPrompt)

    response = box.respond()

    print(response)

    if not response:
        print("Error!  Unable to get input from the model.  Ensure it is working correctly and has a proper connection to needed servers.", file=sys.err)

    if not response.strip().casefold() == "Alpha Bravo Charlie".casefold():
        print("response was not entirely as expected, have a human inspect the prompt!")


if __name__ == "__main__":
    main()
