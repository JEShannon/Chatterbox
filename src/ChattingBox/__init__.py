"""
This Module aims to allow easier use of multiple LLM APIs by handling the API calls, conversations, and key management.

In order to use most of the LLMs you will need an API key, and this module allows for multiple keys being dynamically assigned to models.  This is useful if you have multiple clients using the same backend, so you can monitor usage independantly.

The main exported classes are as follows:

ModelChatter - An empty frame that outlines the functionality of all classes of this module.

GPTChatter - ModelChatter subclass implementing it's features to use the openAI GPT3.5/4 APIs
"""
