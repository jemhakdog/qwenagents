import json
from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    # "llm": {
    #     "model": "ollama/llama3.2",
    #     "temperature": 0,
    #     "format": "json",  
    #     "base_url": "http://localhost:11434",  
    # },
       "llm": {
        "model": "openai/gpt-3.5-turbo-0125",
        "temperature": 0,
        "format": "json",  
        "base_url": "https://www.blackboxapi.com", 
        'api_key': 'EMPTY',
    },
    "embeddings": {
        "model": "ollama/nomic-embed-text",
        "base_url": "http://localhost:11434", 
    }
}


smart_scraper_graph = SmartScraperGraph(
    prompt="Find some information about what does the company do, the name and a contact email.",
    source="https://scrapegraphai.com/",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()
print(json.dumps(result, indent=4))