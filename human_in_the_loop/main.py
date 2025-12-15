from workflows import Context
from workflows.events import InputRequiredEvent, HumanResponseEvent
from human_loop_workflow import HumanInTheLoopWorkflow

async def executeHumanInTheLoopWorkflow():
    workflow = HumanInTheLoopWorkflow()

    handler = workflow.run()

    # listen for InputRequiredEvent
    async for event in handler.stream_events():
        if isinstance(event, InputRequiredEvent):
            # here, we can handle human input however you want
            # this means using input(), websockets, accessing async state, etc.
            # The workflow will wait until the HumanResponseEvent is emitted.
            response = input(event.prefix)
            handler.ctx.send_event(HumanResponseEvent(response=response))

    final_result = await handler
    return (final_result)


async def executeWithLongerWaitPeriod():
    workflow = HumanInTheLoopWorkflow()
    handler = workflow.run()
    async for event in handler.stream_events():

        # listen for InputRequiredEvent
        if isinstance(event, InputRequiredEvent):
            # Serialize the context, store it anywhere as a JSON blob
            ctx_dict = handler.ctx.to_dict()

            print("context stored ", ctx_dict)

            await handler.cancel_run()
            break

    # this workflow.run has stopped running entirely

    # now we handle the human response (the workflow is NOT waiting)
    # here we can use a LlamaIndexUI or any other method to get human input
    response = input(event.prefix)

    # we restart the workflow.run with the context we saved
    restored_ctx = Context.from_dict(workflow, ctx_dict)
    handler = workflow.run(ctx=restored_ctx)

    # And send the human input as event to resume the workflow
    handler.ctx.send_event(HumanResponseEvent(response=response))

    # now we resume the workflow streaming with our restored context
    async for event in handler.stream_events():
        print("continuing with event...", event)
        continue

    final_result = await handler
    return final_result


async def main():
    result = await executeHumanInTheLoopWorkflow()
    print(result)

    result = await executeWithLongerWaitPeriod()
    print(result)


if __name__ == "__main__":
    import asyncio
    print("Testing parallel workflows")
    asyncio.run(main())
    