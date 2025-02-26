import os
from dotenv import load_dotenv
from colorama import Fore
from dataclasses import dataclass
from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel

# Initialize model
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Pydantic model for Movie
@dataclass
class Movie:
    title: str
    year: int
    rating: float
    genre: str
    cast: list[str]

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

# Define the main loop
def main_loop():
    system_prompt = "You are a movie critic and expert."
    agent = Agent(model=get_model("llama-3.3-70b-versatile"), result_type=Movie, system_prompt=system_prompt)
    while True:
        user_input = input(">> Enter a movie query (q, quit, exit to exit): ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break
        result = agent.run_sync(user_input)
        print(Fore.YELLOW, result.data)

if __name__ == "__main__":
    main_loop()

# FastAPI endpoint method
async def getMovieDetails(q: str, model: str, prompt: str) -> Movie:
    model_name = model if not None else "llama-3.3-70b-versatile"
    system_prompt = prompt if not None else "You are a movie critic and expert."
    agent = Agent(model=get_model(model_name), result_type=Movie, system_prompt=system_prompt)
    result = await agent.run(q)
    return result.data