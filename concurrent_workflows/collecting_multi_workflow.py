from workflows import Workflow, Context, step
from workflows.events import Event, StartEvent, StopEvent

class StepAEvent(Event):
    query: str

class StepBEvent(Event):
    query: str

class StepCEvent(Event):
    query: str

class StepACompleteEvent(Event):
    result: str

class StepBCompleteEvent(Event):
    result: str

class StepCCompleteEvent(Event):
    result: str


class ConcurrentFlow(Workflow):
    '''
    start is now declared as emitting 3 different event types
    step_three is now declared as accepting 3 different event types
    collect_events now takes an array of the event types to wait for
    Note that the order of the event types in the array passed to collect_events is important. 
    The events will be returned in the order they are passed to collect_events, regardless of when they were received.
    '''
    @step
    async def start(
        self, ctx: Context, ev: StartEvent
    ) -> StepAEvent | StepBEvent | StepCEvent | None:
        
        # we can launch events of different types in parallel
        ctx.send_event(StepAEvent(query="Query 1"))
        ctx.send_event(StepBEvent(query="Query 2"))
        ctx.send_event(StepCEvent(query="Query 3"))

    @step
    async def step_a(self, ctx: Context, ev: StepAEvent) -> StepACompleteEvent:
        print("Doing something A-ish")
        return StepACompleteEvent(result=ev.query)

    @step
    async def step_b(self, ctx: Context, ev: StepBEvent) -> StepBCompleteEvent:
        print("Doing something B-ish")
        return StepBCompleteEvent(result=ev.query)

    @step
    async def step_c(self, ctx: Context, ev: StepCEvent) -> StepCCompleteEvent:
        print("Doing something C-ish")
        return StepCCompleteEvent(result=ev.query)

    @step
    async def step_three(
        self,
        ctx: Context,
        ev: StepACompleteEvent | StepBCompleteEvent | StepCCompleteEvent,
    ) -> StopEvent:
        print("Received event ", ev.result)

        # collect_events will wait until we receive 3 events
        result = ctx.collect_events(ev, [StepCCompleteEvent, StepACompleteEvent, StepBCompleteEvent])
        if(result is None):
            return None

        # do something with all 3 results together
        return StopEvent(result=result)