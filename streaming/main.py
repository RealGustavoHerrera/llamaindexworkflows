from workflow_streaming import WorkflowStreaming, ProgressEvent

async def main():
    w = WorkflowStreaming(timeout=120, verbose=True)

    handler = w.run(first_input="Start the workflow.")

    # listening for stream events
    async for ev in handler.stream_events():
        if isinstance(ev, ProgressEvent):
            print(ev.msg)

    # receiving final results
    final_result = await handler
    print("Final result", final_result)


if __name__ == "__main__":
    import asyncio
    print("Testing streaming in workflows")
    asyncio.run(main())