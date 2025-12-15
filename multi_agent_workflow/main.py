from dotenv import load_dotenv
from telemetry import setup_telemetry
from llama_index.core.agent.workflow import AgentWorkflow
from llama_index.core.agent.workflow import (
AgentOutput,
ToolCall,
ToolCallResult,
)
from maw_agents import research_agent, write_agent, review_agent

load_dotenv()

async def main():
    # setup telemetry
    await setup_telemetry(project_name="my-llamaindex-workflows-multi-agent")

    # create the agent
    agent_workflow = AgentWorkflow(
    agents=[research_agent, write_agent, review_agent],
    root_agent=research_agent.name,
    initial_state={
        "research_notes": {},
        "report_content": "Not written yet.",
        "review": "Review required.",
        },
    )

    # run the agent workflow with streaming
    handler = agent_workflow.run(
        user_msg=(
            "Write me a report on the history of the internet. "
            "Briefly describe the history of the internet, including the development of the internet, the development of the web, "
            "and the development of the internet in the 21st century."
        ), stream=True
    )

    current_agent = None
    async for event in handler.stream_events():
        if (
            hasattr(event, "current_agent_name")
            and event.current_agent_name != current_agent
            # this is a different agent, print header
        ):
            current_agent = event.current_agent_name
            print(f"\n{'='*50}")
            print(f"🤖 Agent: {current_agent}")
            print(f"{'='*50}\n")

        elif isinstance(event, AgentOutput):
            # the event is an agent output and could contain response.content and/or tool calls
            if event.response.content:
                # it has response content
                print("📤 Output:", event.response.content)
            if event.tool_calls:
                # it has tool calls
                print(
                    "🛠️  Planning to use tools:",
                    [call.tool_name for call in event.tool_calls],
                )
        elif isinstance(event, ToolCallResult):
            # the event is a tool call result
            print(f"🔧 Tool Result ({event.tool_name}):")
            print(f"  Arguments: {event.tool_kwargs}")
            print(f"  Output: {event.tool_output}")
        elif isinstance(event, ToolCall):
            # the event is a tool call
            print(f"🔨 Calling Tool: {event.tool_name}")
            print(f"  With arguments: {event.tool_kwargs}")

    # Workflow has completed - the `async for loop` exits when StopEvent is delivered
    print("\n" + "="*50)
    print("✅ Workflow Complete!")
    print("="*50 + "\n")

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