import streamlit as st
from typing import Literal, Optional, List, Dict, Any
import json
from datetime import datetime

def language_selector() -> str:
    """Display language selection dropdown"""
    return st.selectbox(
        "Select Language",
        ["English", "Spanish", "French", "German", "Italian"],
        index=0
    )

def proficiency_slider() -> int:
    """Display proficiency level slider"""
    return st.slider(
        "Select Proficiency Level",
        min_value=1,
        max_value=5,
        value=3,
        help="1: Beginner, 5: Advanced"
    )

def session_type_selector() -> str:
    """Display session type selection"""
    return st.selectbox(
        "Session Type",
        ["Free Conversation", "Grammar Practice", "Vocabulary Building", "Pronunciation"],
        index=0
    )

def topic_input() -> str:
    """Display topic input field"""
    return st.text_input(
        "Topic (optional)",
        placeholder="Enter a topic for conversation"
    )

def grammar_format_selector() -> str:
    """Display grammar format selection"""
    return st.selectbox(
        "Grammar Feedback Format",
        ["Simple", "Detailed", "Advanced"],
        index=1
    )

def chat_interface(messages: list[dict]):
    """Display chat messages with appropriate styling"""
    for msg in messages:
        is_user = msg["role"] == "user"
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
            if not is_user and msg.get("corrections"):
                with st.expander("View Corrections"):
                    st.json(json.loads(msg["corrections"]))

def message_input() -> str:
    """Display message input field"""
    return st.chat_input("Type your message here...")

def conversation_controls() -> str:
    """Display conversation control buttons"""
    cols = st.columns(3)
    with cols[0]:
        if st.button("Reset Conversation"):
            return "reset"
    with cols[1]:
        if st.button("Export Chat"):
            return "export"
    with cols[2]:
        if st.button("Change Topic"):
            return "change_topic"
    return None

def feedback_settings():
    """Display feedback settings"""
    st.checkbox("Grammar Corrections", value=True, key="grammar_feedback")
    st.checkbox("Vocabulary Suggestions", value=True, key="vocab_feedback")
    st.checkbox("Style Improvements", value=False, key="style_feedback")
    st.checkbox("Cultural Notes", value=False, key="cultural_feedback")