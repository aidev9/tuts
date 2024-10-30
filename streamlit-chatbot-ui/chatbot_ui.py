import streamlit as st
from chat import retrieval_chain

# Constants
height = 600
title = "My Chatbot UI"
icon = ":robot:"

def generate_message(user_input):
    response = retrieval_chain.invoke({"input": user_input})
    answer = response["answer"]

    st.session_state.conversation.append({
        "user": user_input,
        "assistant": answer
    })

    # Iterate over the conversation history
    for entry in st.session_state.conversation:
        messages.chat_message("user").write(entry['user'])
        messages.chat_message("assistant").write(entry['assistant'])

# Session: Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# Set page title and icon
st.set_page_config(page_title=title, page_icon=icon)

def toggle_clicked():
    if st.session_state.clicked is True:
        st.session_state.clicked = False
    else:
        st.session_state.clicked = True

col1, col2 = st.columns([4, 1], gap="large", vertical_alignment="bottom" )
with col1:
    st.header(title)
with col2:
    if st.session_state.clicked is True:
        st.button("Close Files", on_click=toggle_clicked)
    else:
        st.button("Upload Files", on_click=toggle_clicked)

if st.session_state.clicked:
    uploaded_files = st.file_uploader(
        "Upload multiple PDF files into the vector store", accept_multiple_files=True
    )

    for uploaded_file in uploaded_files:
        # write the uploaded file to the data directory
        with open(f"data/{uploaded_file.name}", "wb") as f:
            f.write(uploaded_file.getbuffer())
        # clear the uploaded file
        uploaded_file = None

messages = st.container(border=True, height=height)

if prompt := st.chat_input("Enter your question...", key="prompt"):
    generate_message(prompt)
