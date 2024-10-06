
from duckduckgo_search import DDGS
import json
from qwen_agent.tools.base import BaseTool, register_tool
import json5

@register_tool('my_search_tool')
class MySearchTool(BaseTool):
    description ='search for information in the internet'
    parameters = [
        {
            'name': 'query',
            'type': 'string',
            'description': 'The query to search for in the internet',
            'required': True
        },
        {
            'name': 'max_results',
            'type': 'int',
            'description': 'max number of results to return',
            'required': False
        },
    ]

    def call(self, params: str, **kwargs) -> str:
        query = json.loads(params)['query']
        max_results = json.loads(params).get('max_results', 5)
        results = DDGS().text(query, max_results=max_results)
        return json.dumps(results)
