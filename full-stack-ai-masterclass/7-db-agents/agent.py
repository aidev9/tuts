import os
from dotenv import load_dotenv
from colorama import Fore
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.groq import GroqModel
from supabase import create_client, Client

# Initialize model
load_dotenv()
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")

# Initialise Supabase client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Pydantic model for Customer
@dataclass
class Customer:
    id: str
    email: str
    full_name: str
    bio: str

if not GROQ_API_KEY:
    raise ValueError(
        Fore.RED + "Groq API key not found. Please set the GROQ_API_KEY environment variable."
    )

def get_model(model_name:str):
    try:
        model = GroqModel(
            model_name=model_name,
            api_key=GROQ_API_KEY)
    except Exception as e:
        print(Fore.RED + "Error initializing model: ", e)
        model = None
    
    return model

system_prompt = "You are a customer service agent for a tech company. Use the tools provided to assist customers with their queries."
agent = Agent(model=get_model("llama-3.3-70b-versatile"), result_type=Customer, system_prompt=system_prompt)

# Create tool
@agent.tool(retries=3)
async def create_customer(ctx: RunContext[Client], email: str, full_name: str, bio: str):
    """Create a customer record from the data provided."""
    
    try:
        response = (
            ctx.deps.table("customers")
            .insert([
                {"email": email, "full_name": full_name, "bio": bio}
            ])
            .execute()
        )
        return response
    except Exception as exception:
        return exception

# Retrieve tool
@agent.tool(retries=3)
async def get_customer_by_email(ctx: RunContext[Client], email: str):
    """Retrieve a customer record from their email address."""
    
    response = (
        ctx.deps.table("customers")
        .select("*")
        .eq("email", email)
        .execute()
    )
    
    if response.data:
        return response.data[0]
    else:
        raise ValueError(f"No customer found with email: {email}")
    
# Update tool
@agent.tool(retries=3)
async def update_customer_by_email(ctx: RunContext[Client], email: str, full_name: str, bio: str):
    """Update a customer record from their email address."""
    
    response = (
        ctx.deps.table("customers")
        .update({"full_name": full_name, "bio": bio})
        .eq("email", email)
        .execute()
    )
    
    return response

# Delete tool
@agent.tool(retries=3)
async def delete_customer_by_email(ctx: RunContext[Client], email: str):
    """Delete a customer record from their email address."""
    
    response = (
        ctx.deps.table("customers")
        .delete()
        .eq("email", email)
        .execute()
    )
    
    return response

# Seed function to create table in Supabase, populate with sample data
def seed_db():
    try:
        response = (
            supabase.table("customers")
            .insert([
                {"email": 'johndoe@gmail.com', "full_name": "John Doe", "bio": "I am a software engineer"},
                {"email": 'janedoe@gmail.com', "full_name": "Jane Doe", "bio": "I am a data scientist"},
                {"email": 'jimdoe@gmail.com', "full_name": "Jim Doe", "bio": "I am a product manager"},
            ])
            .execute()
        )
        return response
    except Exception as exception:
        return exception

# Define the main loop
def main_loop():
    # Create a connection to Supabase
    seed_db()
    while True:
        user_input = input(">> Enter a query (q, quit, exit to exit): ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        
        try:
            result = agent.run_sync(user_input, deps=supabase)
            print(Fore.YELLOW, result.data)
        except ValueError:
            print(Fore.RED, "No customer found with that email.")
        except Exception as e:
            print(Fore.RED, "An error occurred: ", e)

if __name__ == "__main__":
    main_loop()