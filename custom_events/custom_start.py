from pathlib import Path

from workflows.events import StartEvent
from llama_index.llms.openai import OpenAI
from pydantic import Field


class CustomStartEvent(StartEvent):
    topic: str = Field(description="The topic to process")
    path_to_save: Path = Field(description="Where to save the result")
    llm: OpenAI = Field(description="The LLM instance to use")

