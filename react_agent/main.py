from telemetry import setup_telemetry
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI
from react_workflow import ReActAgent
from react_tools import tools
from llama_index.core.workflow import Context
from react_events import StreamEvent

load_dotenv()

async def main():
    '''
    https://developers.llamaindex.ai/python/examples/workflow/react_agent/
    with telemetry added
    https://app.arize.com/organizations/QWNjb3VudE9yZ2FuaXphdGlvbjozMTkxNTpYR2g3/spaces/U3BhY2U6MzM1OTk6SE1Rcg==/home
    '''
    await setup_telemetry(project_name="my-llamaindex-workflows-react-agent")

    agent = ReActAgent(
        llm=OpenAI(model="gpt-4o"), tools=tools, timeout=120, verbose=True
    )
    # the agent can preserve state via the context
    ctx = Context(agent)

    # initial message to set up memory
    ret = await agent.run(input="Hello!", ctx=ctx)
    print(ret["response"])

    # example math question
    ret = await agent.run(input="What is (2123 + 2321) * 312?", ctx=ctx)
    print(ret["response"])

    # example with streaming
    handler = agent.run(input="Hello! Tell me a short story with a happy ending.", ctx=ctx, stream=True)

    async for event in handler.stream_events():
        if isinstance(event, StreamEvent):
            print(event.delta, end="", flush=True)

    # full response will also be available after streaming is done
    # response = await handler
    # print(response["response"])


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())