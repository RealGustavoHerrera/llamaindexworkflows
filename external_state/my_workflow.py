from workflows import Workflow, step, Context
from workflows.events import (
    StartEvent,
    StopEvent,
)

class MyWorkflow(Workflow):

    @step
    async def my_step(self, ctx: Context, ev: StartEvent) -> StopEvent:
       # if no ctx is passed, it'll create one with default=0
       current_count = await ctx.store.get("count", default=0)
       current_count += 1
       print(f"storing count: {current_count}")
       await ctx.store.set("count", current_count)
       return StopEvent(result=current_count)
