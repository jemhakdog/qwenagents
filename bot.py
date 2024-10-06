from qwen_agent.agents import Assistant
from ytdl import *
from shell_tool import *
from browser_tools import *
from app_manager import *

from tools.file_manager import FileManager
from tools.image_search import MyImageSearcher
from tools.video_search import MyVideoSearcher
from tools.news_search import MyNewsSearcher
from tools.downloader import MyFileDownloader

llm_cfg = {
    'model': 'llama3.2',
   #'model_server': 'http://127.0.0.1:/8000',
     'model_server': 'https://www.blackboxapi.com',
     #'model_server': 'http://127.0.0.1:11434/v1',
    'api_key': 'EMPTY',
    'generate_cfg': {
        'top_p': 0.8#
    }
}

system_instruction = '''You are a helpful assistant,please do not call same function twice. with same input.'''

tools = [ 
    'my_image_gen', 'code_interpreter', 'my_search_tool',
    'youtube_downloader','my_shell_tool','app_manager',
    'web_browser',"my_image_searcher",'my_video_searcher',
    'my_news_searcher','file_management','my_file_downloader'

      
] 

files = []

bot = Assistant(
    llm=llm_cfg,
    system_message=system_instruction,
    function_list=tools,
    files=files
)