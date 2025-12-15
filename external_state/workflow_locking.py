from pydantic import BaseModel, Field
from workflows import Workflow, step, Context
from workflows.events import (
    StartEvent,
    StopEvent,
)

class CounterState(BaseModel):
    '''
    for Context use a pydantic model that has defaults for all fields. 
    This enables the Context object to automatically initialize the state with the defaults.
    '''
    count: int = Field(default=0)

class WorkflowLocking(Workflow):
    
    @step
    async def start(
        self,
        ctx: Context[CounterState], # pass the context type as the context
        ev: StartEvent
    ) -> StopEvent:
        
        print(f"received counter: {ev.count}")

        # Allows for atomic state updates 
        # (`with edit_state()` locks the state)
        async with ctx.store.edit_state() as ctx_state:
            ctx_state.count = ev.count
            print(f"ctx_state.count is {ctx_state.count}")

        return StopEvent(result="Done!")
