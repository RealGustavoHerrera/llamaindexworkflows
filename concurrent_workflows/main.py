from parallel_workflow import ParallelWorkflow
from collecting_workflow import CollectFlow
from collecting_multi_workflow import ConcurrentFlow

async def main():
    print("Same event in parallel, race condition. First finished returns")
    w = ParallelWorkflow()
    handler = w.run()
    # receiving results
    result = await handler
    print("Result", result)

    print("Same event in parallel, race condition. Wait for all (3) to finish")
    w = CollectFlow()
    handler = w.run()
    # receiving results
    result = await handler
    print("Result", result)

    print("Different events in parallel. Wait for all (3) to finish")
    w = ConcurrentFlow()
    handler = w.run()
    # receiving results
    result = await handler
    print("Result", result)


if __name__ == "__main__":
    import asyncio
    print("Testing parallel workflows")
    asyncio.run(main())