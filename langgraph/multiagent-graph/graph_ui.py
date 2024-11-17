import streamlit as st
from main import graph
from langchain_core.messages import AIMessage, HumanMessage

# Constants
height = 600
title = "Multi-Agent Software Team (LangGraph)"
icon = ":robot:"

def generate_message(user_input):
    response = graph.invoke({"messages": [HumanMessage(content=user_input)]})
    ai_messages = [msg for msg in response["messages"] if isinstance(msg, AIMessage)]

    st.session_state.conversation.append({
        "user": user_input,
        "analyst": ai_messages[-7].content,
        "architect": ai_messages[-6].content,
        "developer": ai_messages[-5].content,
        "reviewer": ai_messages[-4].content,
        "tester": ai_messages[-3].content,
        "diagram_designer": ai_messages[-2].content,
        "summary_writer": ai_messages[-1].content,
    })

    # Iterate over the conversation history
    for entry in st.session_state.conversation:
        messages.chat_message("user", avatar="img/user.png").write(entry['user'])
        messages.chat_message("ai", avatar="img/analyst.png" ).write("**Analyst:** \n" + entry['analyst'])
        messages.chat_message("ai", avatar="img/architect.png" ).write("**Architect:** \n" + entry['architect'])
        messages.chat_message("ai", avatar="img/developer.png" ).write("**Developer:** \n" + entry['developer'])
        messages.chat_message("ai", avatar="img/review.png").write("**Code Reviewer:** \n" + entry['reviewer'])
        messages.chat_message("ai", avatar="img/tester.png" ).write("**Tester:** \n" + entry['tester'])
        messages.chat_message("ai", avatar="img/diagram.png").write("**Diagram Designer:** \n" + entry['diagram_designer'])
        messages.chat_message("ai", avatar="img/summary.png").write("**Summary Writer:** \n" + entry['summary_writer'])

# Session: Initialize conversation history
if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Set page title and icon
st.set_page_config(page_title=title, page_icon=icon)
st.header(title)

# Create a container for the chat messages
messages = st.container(border=True, height=height)

# Chatbot UI
if prompt := st.chat_input("Enter your question...", key="prompt"):
    generate_message(prompt)
