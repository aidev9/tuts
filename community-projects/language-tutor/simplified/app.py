import streamlit as st
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelMessage
)
from pydantic_ai.models.groq import GroqModel
import os
from dotenv import load_dotenv
import asyncio

MODEL_CHOICE = st.selectbox(
    "Select a model",
    ["Llama3.2", "DeepSeek"]
)

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

if MODEL_CHOICE == "Llama3.2":
    model = GroqModel(
        model_name='llama-3.3-70b-versatile',
        api_key=GROQ_API_KEY
    )
elif MODEL_CHOICE == "DeepSeek":
    model = GroqModel(
        model_name='deepseek-r1-distill-llama-70b',
        api_key=GROQ_API_KEY
    )

class AIResponse(BaseModel):
    content: str
    corrections: str

LANGUAGE = st.selectbox("Select a language", [
    "English",
    "Spanish",
    "French",
])

PROFICIENCY = st.slider(
    "Select Proficiency Level",
    min_value=1,
    max_value=5,
    value=3,
    help="1: Beginner, 5: Advanced"
)

agent = Agent(
    model=model,
    result_type=AIResponse,
    system_prompt=(
        f"""
        You are a language tutor helping someone learn {LANGUAGE}.
        Their proficiency level is {PROFICIENCY} out of 5.

        Analyze their message and respond appropriately in {LANGUAGE}.
        Also provide corrections and suggestions if needed.
        """
    )
)

MODEL_AVATARS = {
    "Llama3.2": "🦙",
    "DeepSeek": "🦖"
}

st.title("Simple Sample")
st.caption("Testing it out")

if st.button("New Chat", help="Start a new conversation", use_container_width=True):
    st.session_state.messages = []
    st.session_state.message_history = []
    st.rerun()

if "message_history" not in st.session_state:
    st.session_state["message_history"]: list[ModelMessage] = []

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = MODEL_AVATARS[message.get("model")] if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if "corrections" in message:
            st.markdown("---")
            st.markdown(message["corrections"])

if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.spinner("Generating response..."):
            # Event Loop Management
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            # Execute async operation
            result = loop.run_until_complete(
                agent.run(
                    prompt, 
                    message_history=st.session_state["message_history"]
                )
            )

            # Update message history
            st.session_state["message_history"].extend(result.new_messages())

            print("\n[bold]Message History:[/bold]")
            for i, msg in enumerate(st.session_state["message_history"]):
                print(f"\n[yellow]--- Message {i+1} ---[/yellow]")
                print(msg)
        
        with st.chat_message("assistant"):
            st.markdown(result.data.content)
            st.markdown("---")
            st.markdown(result.data.corrections)

        # Add to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": result.data.content,
            "corrections": result.data.corrections,
            "model": MODEL_CHOICE
        })
    
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})