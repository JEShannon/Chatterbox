import src.ChattingBox.GPTChatter as gptchat
import tests.ChattingBox.gptTest as gpt_test


#The point of this file is to run the tests located in the tests/ChattingBox/gptTest.py
def runTests():
    testsRun = 0
    testsFail = 0
    #run the tests one by one, recording if they succeed
    #contextTest
    testsFail += 0 if gpt_test.contextTest(gptchat.GptBox()) else 1
    testsRun += 1
    #keyTest
    testsFail += 0 if gpt_test.keyTest(gptchat.GptBox()) else 1
    testsRun += 1
    #transcriptTest
    testsFail += 0 if gpt_test.transcriptTest(gptchat.GptBox()) else 1
    testsRun += 1
    if testsFail:
        print("Warning! ", testsFail, "tests failed out of", testsRun, "")
    else:
        print("All", testsRun, "test sets completed!")
    pass


if __name__ == "__main__":
    runTests()
