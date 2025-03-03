import asyncio
import os
import aiosqlite
from sqlite3 import Connection
from colorama import Fore
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel

load_dotenv()

# Define the model
model = OpenAIModel('gpt-4o-mini', api_key=os.getenv('OPENAI_API_KEY'))

class Patient(BaseModel):
    patient_id: int
    email: str
    full_name: str
    year_born: int

# Define the agent
agent = Agent(model=model, system_prompt="You are a helpful medical assistant. Retrieve the patient's record using the tools provided.", result_type=Patient, deps_type=Connection)

@agent.tool(retries=3)
async def get_patient_by_email(ctx: RunContext[Connection], email: str) -> int:
    """Get a patient's record from their email address."""
    
    async with ctx.deps.cursor() as cursor:
        await cursor.execute(f'SELECT * FROM patients WHERE email="{email}"')
        query_result = await cursor.fetchall()
        if not query_result:
            raise ValueError(f"Patient with email {email} not found.")
    return query_result[0]

async def seed_db(conn):
    await conn.execute("DROP TABLE IF EXISTS patients")
    await conn.execute("CREATE TABLE IF NOT EXISTS patients (patient_id INTEGER PRIMARY KEY, email TEXT, full_name TEXT, year_born INTEGER)")
    await conn.execute("INSERT INTO patients (email, full_name, year_born) VALUES ('john@gmail.com', 'John Doe', 1980)")
    await conn.execute("INSERT INTO patients (email, full_name, year_born) VALUES ('jane@gmail.com', 'Jane Doe', 1985)")
    await conn.execute("INSERT INTO patients (email, full_name, year_born) VALUES ('james@gmail.com', 'Jim Doe', 1990)")
    await conn.commit()

async def main():
    async with aiosqlite.connect("patients.sqlite") as conn:
        await seed_db(conn)
        try:
            result = await agent.run('Retrieve the patient record for jane@gmail.com', deps=conn)
            print(Fore.GREEN, f"Patient record: {result.data}")
        except ValueError as e:
            print(Fore.YELLOW, e)
        except Exception as e:
            print(Fore.RED, e)

if __name__ == "__main__":
    asyncio.run(main())