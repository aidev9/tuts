import os
import asyncio
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent
from pydantic_ai.messages import (
    PartDeltaEvent,
    TextPartDelta,
)

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
agent = Agent(model=model, system_prompt="You are a helpful assistant")
user_prompt = 'Create a poem based on cherry blossoms.'

async def main():
    # Begin a node-by-node, streaming iteration
    async with agent.iter(user_prompt) as run:
        async for node in run:
            if Agent.is_model_request_node(node):
                async with node.stream(run.ctx) as request_stream:
                    async for event in request_stream:
                        if isinstance(event, PartDeltaEvent):
                            if isinstance(event.delta, TextPartDelta):
                                print(Fore.GREEN, event.delta.content_delta, sep="", end="", flush=True)
                        

if __name__ == '__main__':
    asyncio.run(main())