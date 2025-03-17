
import time
import streamlit as st
from agent import agent

# Constants
height = 600
title = "Streaming Chatbot"
icon = ":robot:"

# Set page title and icon
st.set_page_config(page_title=title, page_icon=icon)
st.header(title)  

def generate_message(user_input):
    response = agent.run_sync(user_input)
    return response.data

# Streamed response emulator
def response_generator():
    response = generate_message(prompt if prompt is not None else "Hello.")
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(response_generator())

# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})