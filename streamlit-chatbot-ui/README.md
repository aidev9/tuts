## Streamlit Chatbot UI

### Run the app

- Open a terminal and run `python chatbot_ui.py`

- Open a second terminal and run `python ingest.py`

- Upload a PDF file

- Wait for the ingestion to finish

- Ask questions

### Tweaks

- Change the chunk and overlap in [`ingest.py`](./ingest.py) and observe search results. Defaults are:

  - `chunk_size = 1000`
  - `chunk_overlap = 50`

- Change the models from Ollama to OpenAI or another model by adding them to [`models.py`](./models.py) first and then changing the `embeddings` and `llm` references in [`ingest.py`](./ingest.py) and [`chat.py`](./chat.py)
