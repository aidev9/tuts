import os
import logfire
import asyncio
import aiosqlite
from sqlite3 import Connection, Error
from typing import Union
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel
from dotenv import load_dotenv
from colorama import Fore

load_dotenv()

# Configure logfire
logfire.configure()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

class Success(BaseModel):
    sql_query: str

class InvalidRequest(BaseModel):
    error_message: str

Response = Union[Success, InvalidRequest]

agent: Agent[Connection, Response] = Agent(
    model=model,
    result_type=Response,  # type: ignore
    deps_type=Connection,
    system_prompt='Generate SQLite-flavored SQL queries based on user input.',
)

@dataclass
class SQLValidator:
    conn: aiosqlite.Connection

    @agent.result_validator
    async def validate_result(ctx: RunContext[Connection], result_data) -> Response:
        async with ctx.deps.cursor() as cursor:
            await cursor.execute(f'EXPLAIN {result_data.sql_query}')
            explain_result = await cursor.fetchall()
            if not explain_result:
                raise ValueError("Invalid SQL query")
        return result_data

async def main():
    async with aiosqlite.connect("validators.sqlite") as conn:
        await conn.execute("DROP TABLE IF EXISTS users")
        await conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, last_active TIMESTAMP)")
        result = await agent.run("get me users who were last active yesterday.", deps=conn)
        print(Fore.GREEN, result)

if __name__ == "__main__":
    asyncio.run(main())