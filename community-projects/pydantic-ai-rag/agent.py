from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic_ai import RunContext, ModelRetry
from pydantic_ai.usage import UsageLimits
from pydantic import BaseModel, Field
from pydantic_ai.messages import ModelMessage
from vector_store import SupabaseVectorStore
from prompts import rag_prompt,regular_prompt

from dataclasses import dataclass

import os
from dotenv import load_dotenv
import asyncio

# Load environment variables from .env file
load_dotenv()

@dataclass
class Deps:
    store: SupabaseVectorStore


agent_message_history: list[ModelMessage] | None = None

model = GroqModel('llama-3.1-8b-instant', api_key=os.environ.get("GROQ_API_KEY"))
rag_agent = Agent(
    model,
    deps_type = Deps,
)

@rag_agent.tool
async def retrieve(context: RunContext[Deps], search_query: str) -> str:
    if context.deps.store is None:
        return "No data available"
    return await context.deps.store.retrieve_ctx_for_query(search_query)

@rag_agent.system_prompt  
async def get_system_prompt(context: RunContext[Deps]) -> str:  
    if context.deps.store is None:
        return regular_prompt
    return rag_prompt

async def run_agent(query: str, vec_store: SupabaseVectorStore, clear_history: bool = False):
    if clear_history:
        agent_message_history.clear()

    res = await rag_agent.run(
            query,
            message_history=agent_message_history,
            deps=Deps(store=vec_store) 
            )
    return res.data

async def run_test_loop():
    clear_history = False
    while True:
        query = input("User: ")
        if query.lower() in ["quit", "exit", "q"]:
            break

        if query.lower() == "clear":
            clear_history = True

        res = await run_agent(query, SupabaseVectorStore(), clear_history)
        print(f"Agent: {res}")
        clear_history = False


if __name__ == '__main__':
    asyncio.run(run_test_loop())