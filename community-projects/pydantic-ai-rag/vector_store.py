from supabase.client import Client, create_client
from sentence_transformers import SentenceTransformer
import os
import uuid
from dotenv import load_dotenv
import vecs



class SupabaseVectorStore:
    def __init__(self):
        load_dotenv()
        db_url = os.environ.get("DB_URL")
        supabase_key = os.environ.get("SUPABASE_KEY")
        self.__client = create_client(db_url, supabase_key)
        self.__embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L12-v2').to('cpu')
        self.__table_name = "vstore384"

    async def retrieve_ctx_for_query(self,query: str) -> str:
        query_emb = await self.__get_embeddings(query)
        retrieved_docs = self.__match_documents(query_emb)
        return " ".join([doc.content for doc in retrieved_docs])

    async def injest_document(self,content: str, filename: str) -> bool:
        print("Injesting document")
        chunks = self.__split_into_chunks(content)

        documents = []
        for chunk in chunks:
            doc = self.__create_db_document(content,filename)
            documents.append(doc)
        print(documents)

        return self.__insert_into_db(documents)

    def __match_documents(self,query_embedding,filters = None):
        try:
            # Prepare the function parameters
            params = {
                'query_embedding': query_embedding,
                'filters': filters or {}  # Use empty dict if no filters provided
            }
            
            # Call the Supabase stored function
            response = self.__client.rpc(
                'match_documents_vstore384', 
                params=params
            ).execute()
            
            # Return the matched documents
            return response.data
        
        except Exception as e:
            print(f"Error calling match_documents function: {e}")
            return None

    def __insert_into_db(self, documents: list) -> bool:
        try:
            self.__client.table(self.__table_name).insert(documents).execute()
            return True
        except Exception as e:
            print(f"Error in bulk insert: {e}")
            return False
        
    async def __create_db_document(self,content: str, source_file_name: str):
        return {
            'id': str(uuid.uuid4()),
            'content': content,
            'metadata': {
                "source": source_file_name
            },
            'embedding': await self.__get_embeddings(content)
        }
        
    async def __get_embeddings(self,text: str):
        return await self.__embedding_model.encode(text)

    def __split_into_chunks(text, chunk_size=1000, overlap=10):
    
        # Split the text into words
        words = text.split()
        
        # Handle edge cases
        if not words:
            return []
        
        if len(words) <= chunk_size:
            return [' '.join(words)]
        
        chunks = []
        start = 0
        
        while start < len(words):
            # Extract a chunk of words
            chunk_words = words[start:start + chunk_size]
            chunks.append(' '.join(chunk_words))
            
            # Move the start position forward, considering the overlap
            start += chunk_size - overlap
        
        return chunks