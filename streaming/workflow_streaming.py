import os
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

from workflows import (
    Workflow,
    Context,
    step,
)
from workflows.events import (
    StartEvent,
    StopEvent,
    Event,
)

class FirstEvent(Event):
    first_output: str


class SecondEvent(Event):
    second_output: str
    response: str


class ProgressEvent(Event):
    msg: str

class WorkflowStreaming(Workflow):
    @step
    async def step_one(self, ctx: Context, ev: StartEvent) -> FirstEvent:
        print(f"received {ev.first_input}")
        ctx.write_event_to_stream(ProgressEvent(msg="Step one is happening"))
        return FirstEvent(first_output="First step complete.")

    @step
    async def step_two(self, ctx: Context, ev: FirstEvent) -> SecondEvent:
        llm = OpenAI(model="gpt-4o-mini", api_key=OPENAI_API_KEY)
        generator = await llm.astream_complete(
            "Please give me the first 3 paragraphs of Moby Dick, a book in the public domain."
        )
        full_resp = ""
        async for response in generator:
            # Allow the workflow to stream this piece of response
            ctx.write_event_to_stream(ProgressEvent(msg=response.delta))
            full_resp += response.delta

        return SecondEvent(
            second_output="Second step complete, full response attached",
            response=full_resp,
        )

    @step
    async def step_three(self, ctx: Context, ev: SecondEvent) -> StopEvent:
        print(f"Received {ev.second_output}")
        print(f"full response: {ev.response}")
        ctx.write_event_to_stream(ProgressEvent(msg="Step three is happening"))
        return StopEvent(result="Workflow complete.")
    