# Using random to simulate LLM 

import random
from workflows import Workflow, step
from workflows.events import (
    Event,
    StartEvent,
    StopEvent,
)

class BranchA1Event(Event):
    payload: str


class BranchA2Event(Event):
    payload: str


class BranchB1Event(Event):
    payload: str


class BranchB2Event(Event):
    payload: str


class BranchWorkflow(Workflow):
    @step
    async def start(self, ev: StartEvent) -> BranchA1Event | BranchB1Event:
        if random.randint(0, 10) < 5:
            print("Go to branch A")
            return BranchA1Event(payload="Branch A")
        else:
            print("Go to branch B")
            return BranchB1Event(payload="Branch B")

    @step
    async def step_a1(self, ev: BranchA1Event) -> BranchA2Event:
        print(f"{ev.payload} Step 1")
        return BranchA2Event(payload=ev.payload)

    @step
    async def step_b1(self, ev: BranchB1Event) -> BranchB2Event:
        print(f"{ev.payload} Step 1")
        return BranchB2Event(payload=ev.payload)

    @step
    async def step_a2(self, ev: BranchA2Event) -> StopEvent:
        print(f"{ev.payload} Step 2")
        return StopEvent(result="Branch A complete.")

    @step
    async def step_b2(self, ev: BranchB2Event) -> StopEvent:
        print(f"{ev.payload} Step 2")
        return StopEvent(result="Branch B complete.")
    
    

async def main():
    w = BranchWorkflow()
    print("flow created")
    result = await w.run()
    print("we got the results: ")
    print(str(result))

if __name__ == "__main__":
    import asyncio
    print("Trying branching workflows")
    asyncio.run(main())
    