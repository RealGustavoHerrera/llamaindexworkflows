import asyncio
from workflows import Workflow, step
from workflows.events import StartEvent, StopEvent
from workflows.server import WorkflowServer

class MyWorkflow(Workflow):
    @step
    async def my_step(self, ev: StartEvent) -> StopEvent:
        return StopEvent(result="Done!")

async def main():
    print("starting...")

    server = WorkflowServer()
    server.add_workflow("my_workflow", MyWorkflow())
    await server.serve("0.0.0.0", 8000)


if __name__ == "__main__":
    asyncio.run(main())