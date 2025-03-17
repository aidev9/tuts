import os
import asyncio
from dotenv import load_dotenv
from typing_extensions import TypedDict
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

class Recipe(TypedDict, total=False):
    """ A recipe with a name, list of ingredients, and list of instructions. """
    name: str
    ingredients: list[str]
    instructions: list[str]

agent = Agent(
    model=model,
    result_type=Recipe,
    system_prompt='Extract a recipe from the input',
)

async def main():
    user_input = 'Italian creamy pasta carbonara recipe with peppers and bacon.'
    async with agent.run_stream(user_input) as result:
        async for recipe in result.stream():
            print(recipe)

if __name__ == '__main__':
    asyncio.run(main())