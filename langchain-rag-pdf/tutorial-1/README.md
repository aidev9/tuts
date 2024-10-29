## Chat to PDF

### Use your own files

- Check out the tutorial code from [GitHub](https://github.com/aidev9/tuts/tree/main/langchain-rag-pdf/tutorial-1)

- Install the required libraries by running `pip install -r requirements.txt`

- If you haven't installed Ollama, do so by running `brew install ollama` (Mac)

- Pull Llama 3.2 by running `ollama pull llama3.2`

- Pull mxbai-embed-large embedding model by running `ollama pull mxbai-embed-large`

- Drop your PDF files into [`./data`](./data)

- Open a new terminal and ingest your PDF files into ChromaDB by running `python ingest.py`. Leave the terminal open as you can drop more files into the [`./data`](./data) folder and the script will automatically pick them up

- Open a second terminal and run the RAG chatbot with `python chat.py`

- Ask questions

### Tweaks

- Change the chunk and overlap in [`ingest.py`](./ingest.py) and observe search results. Defaults are:

  - `chunk_size = 1000`
  - `chunk_overlap = 50`

- Change the models from Ollama to OpenAI or another model by adding them to [`models.py`](./models.py) first and then changing the `embeddings` and `llm` references in [`ingest.py`](./ingest.py) and [`chat.py`](./chat.py)

### Talk to OWASP Secure Coding Standards

- Delete all files from the [`./data`](./data) folder

- Delete the ChromaDB local files at [`./db`](./db) folder

- Open a new terminal and run `python html-to-pdf.py`. This will scrape the OWASP website and create 10 PDF files inside the [`./data`](./data) folder

- Run the ingestion script

- Ask questions related to secure coding standards
