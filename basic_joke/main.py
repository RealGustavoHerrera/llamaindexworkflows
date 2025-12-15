import os
from dotenv import load_dotenv
from workflows import Workflow, step
from workflows.events import (
    Event,
    StartEvent,
    StopEvent,
)
from llama_index.llms.openai import OpenAI

load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

class JokeEvent(Event):
    '''
    Events are user-defined pydantic objects. 
    You control the attributes and any other auxiliary methods. 
    In this case, our workflow relies on a single user-defined event, the JokeEvent.
    '''
    joke: str


class JokeFlow(Workflow):
    '''
    Our workflow is implemented by subclassing the Workflow class. 
    For simplicity, we attached a static OpenAI llm instance.
    '''
    llm = OpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4.1", 
    )

    @step
    async def generate_joke(self, ev: StartEvent) -> JokeEvent:
        topic = ev.topic

        prompt = f"Write your best joke about {topic}."
        response = await self.llm.acomplete(prompt)
        return JokeEvent(joke=str(response))

    @step
    async def critique_joke(self, ev: JokeEvent) -> StopEvent:
        joke = ev.joke

        prompt = f"Give a thorough analysis and critique of the following joke: {joke}"
        response = await self.llm.acomplete(prompt)
        return StopEvent(result=str(response))

async def main():
    w = JokeFlow(timeout=60, verbose=False)
    print("flow created")
    result = await w.run(topic="pirates")
    print("we got the results: ")
    print(str(result))

if __name__ == "__main__":
    import asyncio
    print("Asking for pirate jokes and critiques")
    asyncio.run(main())
    