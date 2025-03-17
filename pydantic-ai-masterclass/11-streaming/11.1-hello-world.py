import os
import asyncio
from colorama import Fore
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai import Agent

load_dotenv()

# # Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))
agent = Agent(model=model, system_prompt="You are a brilliant poet.", result_type=str)
user_prompt = 'Write a short poem on cherry blossoms.'

async def main():
    async with agent.run_stream(user_prompt=user_prompt) as result:
        async for poem in result.stream():
            print(poem)

if __name__ == '__main__':
    asyncio.run(main())