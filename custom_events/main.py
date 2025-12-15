import os
from pathlib import Path
from dotenv import load_dotenv
from joke_flow import JokeFlow, JokeFlowWithCustomStop
from custom_start import CustomStartEvent
from custom_stop import CustomStopEvent
from llama_index.llms.openai import OpenAI

load_dotenv()


async def tryStartEvent():
    w = JokeFlow(timeout=60, verbose=False)
    print("flow created")

    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4.1", 
    )

    # We could pass the fields of MyCustomStartEvent as keyword arguments to the run method of our workflow, 
    # but that would be cumbersome. 

    #  A better approach is to create a custom start instance and...
    custom_start = CustomStartEvent(topic="pirates", path_to_save=Path("result.txt"), llm=llm)

    # then pass the event instance through the start_event keyword argument like this:
    result = await w.run(start_event=custom_start)
    print("we got the results: ")
    print(str(result))

async def tryStopEvent():
    w = JokeFlowWithCustomStop(timeout=60, verbose=False)

    llm = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4.1", 
    )
    custom_start = CustomStartEvent(topic="pirates", path_to_save=Path("result.txt"), llm=llm)

    # Warning! `result` now contains an instance of CustomStopEvent
    result: CustomStopEvent = await w.run(start_event=custom_start)
    # We can now access the event fields as any normal Event
    print(result.joke.text)

async def main():
    await tryStopEvent()

if __name__ == "__main__":
    import asyncio
    print("Asking for pirate jokes with custom events")
    asyncio.run(main())