import pprint
import urllib.parse
import json5
from qwen_agent.tools.base import BaseTool, register_tool

from tool_list import *
from bot import bot
from qwen_agent.gui import WebUI


def main():
    """
    Main function for the bot.

    This function runs an infinite loop, waiting for user input. For each input, it asks the bot to generate a response and then prints out the response. The conversation history is stored in the messages variable.

    The bot is defined in the bot variable, which is an instance of the Assistant class from the bot module.
    """
    
    messages = []
    while True:
        query = input('user query: ')
        messages.append({'role': 'user', 'content': query})
        response = []
        for response in bot.run(messages=messages):
           print('bot response:')
           pprint.pprint(response, indent=2)
        print(response[-1]['content'])
        messages.extend(response)

def app_gui():
    chatbot_config = {
        'verbose': True,
    }
    WebUI(bot, chatbot_config=chatbot_config).run()


if __name__ == '__main__':
     main()
    #app_gui()
