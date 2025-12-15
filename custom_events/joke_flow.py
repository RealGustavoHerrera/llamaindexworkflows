from workflows import Workflow, step
from workflows.events import StopEvent
from custom_start import CustomStartEvent
from custom_stop import CustomStopEvent

class JokeFlow(Workflow):
    @step
    async def step1 (self, ev: CustomStartEvent) -> StopEvent:
        prompt = f"Write your best joke about {ev.topic}."

        response = await ev.llm.acomplete(prompt)
        # Dump the response on disk using the Path object from the event
        ev.path_to_save.write_text(str(response))
        # Finally, send the StopEvent

        # if we use StopEvent, the result of a workflow must be set to the `result` field of the event instance.
        return StopEvent(result=str(response))
    

class JokeFlowWithCustomStop(Workflow):
    @step
    async def step1 (self, ev:CustomStartEvent) -> CustomStopEvent:
        prompt = f"Write your best joke about {ev.topic}."
        response = await ev.llm.acomplete(prompt)
        # Dump the response on disk using the Path object from the event
        ev.path_to_save.write_text(str(response))
        # Finally, send the CustomStop

        # when using a custom stop event the result of a workflow run will be the instance of the event
        return CustomStopEvent(joke=response)
