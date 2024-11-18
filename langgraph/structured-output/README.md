## Structured Output Parsers

### Video Tutorial

[Watch the video tutorial here](https://youtu.be/GNpXkoOX4Go)

### Setup

- pip install -r requirements.txt
- Create a .env file and add OPENAI, LANGCHAIN keys (Use .env.example as template)
- Review the context limit in LLM declaration [main.py](./main.py)

```python
llm = AzureChatOpenAI(
    azure_deployment=os.environ.get("AZURE_OPENAI_API_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
    temperature=0,
    max_tokens=1000,
    timeout=None,
    max_retries=2,
)
```

### Run

- `python main.py`
