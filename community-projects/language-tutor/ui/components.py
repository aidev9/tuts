import streamlit as st
from typing import Literal, Optional

def language_selector() -> str:
    """Render language selection dropdown"""
    return st.selectbox(
        "Choose a language to learn:",
        ["English", "Spanish", "French", "German", "Italian"],
        key="language_select"
    )

def proficiency_slider() -> int:
    """Render proficiency level slider"""
    return st.slider(
        "Select your proficiency level (1-5):",
        min_value=1,
        max_value=5,
        value=3,
        key="proficiency_slider"
    )

def session_type_selector() -> Literal["conversation", "vocabulary", "grammar"]:
    """Render session type selector"""
    return st.radio(
        "Choose session type:",
        ["Conversation", "Vocabulary", "Grammar"],
        key="session_type"
    ).lower()

def topic_input() -> Optional[str]:
    """Render topic input field"""
    if st.session_state.get("session_type") in ["conversation", "vocabulary"]:
        return st.text_input(
            "Enter a topic (optional):",
            key="topic_input"
        )
    return None

def grammar_format_selector() -> Optional[Literal["fill_in_blank", "multiple_choice"]]:
    """Render grammar format selector"""
    if st.session_state.get("session_type") == "grammar":
        return st.radio(
            "Choose grammar exercise format:",
            ["Fill in the blanks", "Multiple choice"],
            key="grammar_format"
        ).lower().replace(" ", "_")
    return None