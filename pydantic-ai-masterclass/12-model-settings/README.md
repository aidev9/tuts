# Math Tutor AI

A friendly math tutor agent built with PydanticAI that helps primary school students solve math problems.

## Features

- Step-by-step problem solving
- Age-appropriate explanations
- Practice problem suggestions
- Difficulty level assessment
- Basic arithmetic operations (add, subtract, multiply, divide)

## Installation

1. Clone the repository
2. Install dependencies using Poetry:
   ```bash
   poetry install
   ```
3. Copy `.env.example` to `.env` and add your OpenAI and Genimi API keys:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   GEMINI_API_KEY=your_api_key_here
   ```

## Usage

```python
from math_tutor_ai import math_tutor

async def main():
    question = "If I have 5 apples and my friend gives me 3 more, how many apples do I have in total?"
    response = await math_tutor.run(question)
    result = response.data
    print(f"Answer: {result.answer}")
    print(f"Explanation: {result.explanation}")
    print(f"Steps: {result.steps}")
```

## Testing

Run the tests using pytest:

```bash
poetry run python 12.1-hello-world.py
```

## Requirements

- Python 3.12 or higher
- Poetry for dependency management
- OpenAI API key
