import streamlit as st
from parser import parse_pdf
from agent import run_agent
from vector_store import SupabaseVectorStore

import asyncio

vec_store: SupabaseVectorStore = None
warning: str = None
error: str = None

async def chat_loop():
    global vec_store
    global warning
    global error

    input = st.text_input("Your question here..")
    submit_button = st.button("Submit")  # Capture the button press

    # Execute the code only when the button is pressed
    if submit_button:
        if input and input.strip() != "":
            with st.spinner("Getting LLM response.."):
                try:
                    response = await run_agent(input, vec_store)
                    st.text_area("Chatbot response", response, height=400)
                except Exception as e:
                    error = f"Error during chat processing: {e}"
        else:
            warning = "Please enter a question."
    
async def upload_pdf_process(content: str, filename: str):
    global vec_store
    global warning
    global error

    if content is not None:
        with st.spinner("Uploading document.."):
            try:
                if vec_store is None:
                    print("Creating new vector store")
                    vec_store = SupabaseVectorStore()

                print("Injesting")
                success = await vec_store.injest_document(content, filename)
            except Exception as e:
                st.error(f"Error during document ingestion: {e}")
                return
        
        if success:
            await chat_loop()
        else:
            error = "Error with vector store"
    else:
        error = "PDF had no content"
        
    

async def main_loop():    
    global warning
    global error

    st.title("RAG using Pydantic AI")

    if warning:
        st.warning(warning)
    if error:
        st.error(error)
    
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    await chat_loop() 

    # Check if a file was uploaded
    if uploaded_file is not None:
        # Display success message
        st.success(f"File '{uploaded_file.name}' successfully uploaded!")
            
        # Read PDF content
        try:
            with st.spinner("Reading PDF.."):
                upload_file_content, name = parse_pdf(uploaded_file.getvalue())
            await upload_pdf_process(upload_file_content, name)   
                
        except Exception as e:
            error = f"Error reading PDF: {e}"
            

if __name__ == "__main__":
    asyncio.run(main_loop())