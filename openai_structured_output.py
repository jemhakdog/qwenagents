# from pydantic import BaseModel
# from openai import OpenAI
#
# client = OpenAI(base_url="https://www.blackboxapi.com",api_key='aa')
#
# class CalendarEvent(BaseModel):
#     name: str
#     date: str
#     participants: list[str]
#
# completion = client.beta.chat.completions.parse(
#     model="gpt-4o-2024-08-06",
#     messages=[
#         {"role": "system", "content": "Extract the event information."},
#         {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
#     ],
#     response_format=CalendarEvent,
# )
#
# event = completion
# print(event)

from typing import List
from pydantic import BaseModel, Field
from rich.pretty import pprint
from phi.assistant import Assistant
from phi.llm.openai.like import OpenAILike

class MovieScript(BaseModel):
    setting: str = Field(..., description="Provide a nice setting for a blockbuster movie.")
    ending: str = Field(..., description="Ending of the movie. If not available, provide a happy ending.")
    genre: str = Field(..., description="Genre of the movie. If not available, select action, thriller or romantic comedy.")
    name: str = Field(..., description="Give a name to this movie")
    characters: List[str] = Field(..., description="Name of characters for this movie.")
    storyline: str = Field(..., description="3 sentence storyline for the movie. Make it exciting!")

movie_assistant = Assistant(
    llm=OpenAILike(
        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        api_key="aa",
        base_url="https://www.blackboxapi.com",
    ),
    description="You help write movie scripts.",
    output_model=MovieScript,
)

pprint(movie_assistant.run("New York"))
