import streamlit as st
from agent import agent

# Constants
height = 600
title = "Markdown Chatbot"
icon = ":robot:"

def generate_message(user_input):
    response = agent.run_sync(user_input)
    answer = response.data

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
st.header(title)

messages = st.container(border=True, height=height)
if prompt := st.chat_input("Enter your question...", key="prompt"):
    generate_message(prompt)