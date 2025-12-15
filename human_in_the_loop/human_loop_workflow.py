from workflows import Workflow, step
from workflows.events import StartEvent, StopEvent, InputRequiredEvent, HumanResponseEvent

class HumanInTheLoopWorkflow(Workflow):
    '''
    This workflow should run on streaming
    '''
    @step
    async def step1(self, ev: StartEvent) -> InputRequiredEvent:
        print(f"start event received {ev}")
        # in a real case we'd be doing something more complex here
        # and when we find we need human input, we'd emit an InputRequiredEvent
        # we are manually requesting human input here
        return InputRequiredEvent(prefix="Enter a number: ")

    @step
    async def step2(self, ev: HumanResponseEvent) -> StopEvent:

        # we just show the human response here to prove we got it
        print(f"Human response received {ev}")
        return StopEvent(result=ev.response)

