from fastapi import FastAPI
from agent import getMovieDetails

app = FastAPI()

# FastAPI endpoint
@app.get("/getMovieDetails/")
async def get_movie_details_endpoint(q: str | None = None, model: str | None = None, prompt: str | None = None):
    return await getMovieDetails(q, model, prompt)