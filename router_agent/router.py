"""A multi-agent cooperation example implemented by router and assistant"""

import os
from typing import Optional

from qwen_agent.agents import Assistant, ReActChat, Router
from qwen_agent.gui import WebUI

from tools.file_manager import FileManager
from tools.search_tool import MySearchTool
from tools.image_gen import MyImageGen
from tools.image_search import MyImageSearcher
from tools.video_search import MyVideoSearcher
from tools.news_search import MyNewsSearcher
ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')


def init_agent_service():
    # settings
    llm_cfg = {
    'model': 'llama3.2',
   #'model_server': 'http://127.0.0.1:/8000',
    'model_server': 'https://www.blackboxapi.com',
    # 'model_server': 'http://127.0.0.1:11434/v1',
    'api_key': 'EMPTY',
    'generate_cfg': {
        'top_p': 0.8
    }
    }
    tools = ['my_image_gen', 'code_interpreter']
    file_tools = ['file_management']
    search_tools = ['my_search_tool',"my_image_searcher",'my_video_searcher','my_news_searcher']

    bot_vl = ReActChat(llm=llm_cfg, name='assistant', description='you are a helpful assistant always talk in english') 

    bot_tool = Assistant(
        llm=llm_cfg,
        name='Tool Assistant',
        description='can use image generation tools and run code to solve problems',
        function_list=tools,
    )
    file_bot  = Assistant(
        llm=llm_cfg,
        name='file Assistant',
        description='can use tools to manage files and directories in windows', 
        function_list=file_tools,
    )

    searc_bot  = Assistant(
        llm=llm_cfg,
        name='searc Assistant',
        description='can use tools search any information to the internet', 
        function_list=search_tools,
    )

    bot = Router(
        llm=llm_cfg,
        agents=[bot_vl,bot_tool,file_bot,searc_bot],
    )
    return bot


# def app_tui():
#     bot = init_agent_service()
#     messages = []
#     while True:
#         query = input('user question: ')
#         if not query:
#             print('user question cannot be empty！')
#             continue
#         messages.append({'role': 'user', 'content': query})
#         response = []
#         for response in bot.run(messages):
#             print('bot response:', response)
#         messages.extend(response)





# if __name__ == '__main__':
#     app_tui()


def app_gui():
    bot = init_agent_service()
    chatbot_config = {
        'verbose': True,
    }
    WebUI(bot, chatbot_config=chatbot_config).run()


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()