from dotenv import load_dotenv
from llama_index.utils.workflow import (
    draw_all_possible_flows,
    draw_most_recent_execution,
)
from agent_workflow import run_agent_workflow
from telemetry import setup_telemetry

load_dotenv()

async def main():
    # setup telemetry
    await setup_telemetry(project_name="my-llamaindex-workflows-multi-agent")

    # run the agent workflow
    [handler, agent_workflow] = await run_agent_workflow() 

    # Workflow has completed - the `async for loop` exits when StopEvent is delivered
    print("\n" + "="*50)
    print("✅ Workflow Complete!")
    print("="*50 + "\n")

    draw_most_recent_execution(handler, filename="multi_most_recent.html")
    draw_all_possible_flows(agent_workflow, filename="multi_all_flows.html")

    # Access final state after completion
    state = await handler.ctx.store.get("state")

    print("\n >> Research Notes:\n")
    print(state["research_notes"])

    print("\n >> Review:\n")
    print(state["review"])

    print("\n >> Final Report Content:\n")
    print(state["report_content"])


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())