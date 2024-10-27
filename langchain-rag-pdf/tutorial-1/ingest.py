import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from uuid import uuid4
from models import Models

load_dotenv()

# Initialize the models
models = Models()
embeddings = models.embeddings_ollama
llm = models.model_ollama

# Define constants
data_folder = "./data"
chunk_size = 1000
chunk_overlap = 50
check_interval = 10

# Chroma vector store
vector_store = Chroma(
    collection_name="documents",
    embedding_function=embeddings,
    persist_directory="./db/chroma_langchain_db",  # Where to save data locally
)

# Ingest a file
def ingest_file(file_path):
    # Skip non-PDF files
    if not file_path.lower().endswith('.pdf'):
        print(f"Skipping non-PDF file: {file_path}")
        return
    
    print(f"Starting to ingest file: {file_path}")
    loader = PyPDFLoader(file_path)
    loaded_documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, separators=["\n", " ", ""]
    )
    documents = text_splitter.split_documents(loaded_documents)
    uuids = [str(uuid4()) for _ in range(len(documents))]
    print(f"Adding {len(documents)} documents to the vector store")
    vector_store.add_documents(documents=documents, ids=uuids)
    print(f"Finished ingesting file: {file_path}")

# Main loop
def main_loop():
    while True:
        for filename in os.listdir(data_folder):
            if not filename.startswith("_"):
                file_path = os.path.join(data_folder, filename)
                ingest_file(file_path)
                new_filename = "_" + filename
                new_file_path = os.path.join(data_folder, new_filename)
                os.rename(file_path, new_file_path)
        time.sleep(check_interval)  # Check the folder every 10 seconds

# Run the main loop
if __name__ == "__main__":
    main_loop()