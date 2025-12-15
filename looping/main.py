# Using random to simulate LLM 

import random
from workflows import Workflow, step
from workflows.events import (
    Event,
    StartEvent,
    StopEvent,
)

class LoopEvent(Event):
    num_loops: int


class LoopingWorkflow(Workflow):
    @step
    async def prepare_input(self, ev: StartEvent) -> LoopEvent:
        num_loops = random.randint(0, 10)
        print(f"looping {num_loops+1} times")
        return LoopEvent(num_loops=num_loops)

    @step
    async def loop_step(self, ev: LoopEvent) -> LoopEvent | StopEvent:
        print (f"this is loop: {ev.num_loops}")
        if ev.num_loops <= 0:
            return StopEvent(result="Done looping!")

        return LoopEvent(num_loops=ev.num_loops-1)


async def main():
    w =  LoopingWorkflow()
    print("flow created")
    result = await w.run()
    print("we are done!")
    print(str(result))

if __name__ == "__main__":
    import asyncio
    print("Testing looping workflows")
    asyncio.run(main())
    