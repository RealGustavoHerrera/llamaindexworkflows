from workflows.events import StopEvent
from llama_index.core.llms import CompletionResponse
from pydantic import Field

class CustomStopEvent(StopEvent):
    joke: CompletionResponse = Field(description="The joke result of the LLM call")