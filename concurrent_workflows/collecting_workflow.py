import asyncio
import random
from workflows import Workflow, Context, step
from workflows.events import Event, StartEvent, StopEvent

class StepTwoEvent(Event):
    query: str

class StepThreeEvent(Event):
    result: str

class CollectFlow(Workflow):
    @step
    async def start(self, ctx: Context, ev: StartEvent) -> StepTwoEvent | None:
        print("received start event ", ev)
        # we can launch the same event multiple times in parallel
        ctx.send_event(StepTwoEvent(query="Query 1"))
        ctx.send_event(StepTwoEvent(query="Query 2"))
        ctx.send_event(StepTwoEvent(query="Query 3"))

    @step(num_workers=4)
    async def step_two(self, ctx: Context, ev: StepTwoEvent) -> StepThreeEvent:
        print("Running query ", ev.query)
        await asyncio.sleep(random.randint(1, 5))
        return StepThreeEvent(result=ev.query)

    @step
    async def step_three(
        self, ctx: Context, ev: StepThreeEvent
    ) -> StopEvent | None:
        '''
        The collect_events method lives on the Context and takes the event that triggered the step and 
        an array of event types to wait for.
        In this case, we are awaiting 3 events of the same StepThreeEvent type.
        
        :param self: Description
        :param ctx: Description
        :type ctx: Context
        :param ev: Description
        :type ev: StepThreeEvent
        :return: Description
        :rtype: StopEvent | None
        '''
        # collect_events will wait until we receive 3 events
        result = ctx.collect_events(ev, [StepThreeEvent] * 3)
        if result is None:
            return None
        # The result returned from collect_events is an array of the events that were collected, 
        # in the order that they were received.
        print(result)
        return StopEvent(result="Done")