from llama_index.core.llms import ChatMessage
from llama_index.core.tools import ToolSelection, ToolOutput
from llama_index.core.workflow import Event

'''
An event to handle new messages and prepare the chat history
An event to stream the LLM response
An event to prompt the LLM with the react prompt
An event to trigger tool calls, if any
An event to handle the results of tool calls, if any
The other steps will use the built-in StartEvent and StopEvent events.
'''

class PrepEvent(Event):
    pass


class InputEvent(Event):
    input: list[ChatMessage]


class StreamEvent(Event):
    delta: str


class ToolCallEvent(Event):
    tool_calls: list[ToolSelection]


class FunctionOutputEvent(Event):
    output: ToolOutput