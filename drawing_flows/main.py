import os
from pathlib import Path

from concurrent_workflows.collecting_multi_workflow import ConcurrentFlow

from llama_index.utils.workflow import (
    draw_all_possible_flows,
    draw_most_recent_execution,
)

async def main():
    # Change to the draw directory so lib/ is created there
    # we can specify the output for the html files, but the lib/ directory is created in the current working directory
    # and we want to keep the output files in the same directory as the script
    output_dir = Path(__file__).parent / "draw"
    output_dir.mkdir(exist_ok=True)
    os.chdir(output_dir)

    # Draw all
    print("drawing all possible flows")
    draw_all_possible_flows(ConcurrentFlow, filename="all_paths.html")

    # Draw an execution
    w = ConcurrentFlow()
    handler = w.run()
    result = await handler
    print(f"Executed, result: {result}")
    print("drawing an execution")
    draw_most_recent_execution(handler, filename="most_recent.html")

if __name__ == "__main__":
    import asyncio
    print("Drawing workflows")
    asyncio.run(main())
    