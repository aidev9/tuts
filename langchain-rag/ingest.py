import os
import time
from dotenv import load_dotenv
from langchain_community.vectorstores import SupabaseVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from supabase.client import Client, create_client

load_dotenv()

# Supabase vector store
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Ollama embeddings model
embeddings = OllamaEmbeddings(
    model="llama3.1"
)

# Define constants
data_folder = "./data"
chunk_size = 1000
chunk_overlap = 10
table_name = "documents"
query_name = "match_documents"
check_interval = 10

# Ingest a file to Supabase
def ingest_file_to_supabase(file_path):
    print(f"Ingesting file: {file_path}")
    loader = TextLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)

    return SupabaseVectorStore.from_documents(
        docs,
        embeddings,
        client=supabase,
        table_name=table_name,
        query_name=query_name,
        chunk_size=chunk_size,
    )

# Main loop
def main_loop():
    while True:
        for filename in os.listdir(data_folder):
            if not filename.startswith("_"):
                file_path = os.path.join(data_folder, filename)
                ingest_file_to_supabase(file_path)
                new_filename = "_" + filename
                new_file_path = os.path.join(data_folder, new_filename)
                os.rename(file_path, new_file_path)
        time.sleep(check_interval)  # Check the folder every 10 seconds

# Run the main loop
if __name__ == "__main__":
    main_loop()