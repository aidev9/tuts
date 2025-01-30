import streamlit as st
from dotenv import load_dotenv
import asyncio
from agent import LanguageTutorAgent
from data import get_db, ConversationRepository
from ui.components import (
    language_selector,
    proficiency_slider,
    session_type_selector,
    topic_input,
    grammar_format_selector,
    chat_interface,
    message_input,
    conversation_controls,
    feedback_settings
)

# Load environment variables
load_dotenv()

# Initialize agent
if "agent" not in st.session_state:
    st.session_state.agent = LanguageTutorAgent()

# Streamlit app configuration
st.set_page_config(
    page_title="Language Tutor",
    page_icon="🗣️",
    layout="wide"
)

async def handle_message(message: str):
    """Handle user message and get agent response"""
    response_data = await st.session_state.agent.process_message(message)
    return response_data

def get_conversation_history():
    """Get conversation history from database"""
    with get_db() as db:
        repo = ConversationRepository(db)
        if hasattr(st.session_state.agent, '_session_id'):
            messages = repo.get_conversation_history(st.session_state.agent._session_id)
            # Reverse the messages to show oldest first
            return list(reversed(messages))
    return []

def main():
    st.title("Language Tutor Agent")
    st.write("Welcome to your personal language learning assistant!")
    
    # Session configuration
    with st.sidebar:
        st.header("Session Configuration")
        language = language_selector()
        level = proficiency_slider()
        session_type = session_type_selector()
        topic = topic_input()
        grammar_format = grammar_format_selector()
        
        start_session = st.button("Start Session")
        if start_session:
            st.session_state.agent.set_language(language)
            st.session_state.agent.set_proficiency(level)
            session = st.session_state.agent.start_session(session_type)
            st.session_state.session = session
            st.success(f"Started {session_type} session in {language} at level {level}")
            st.rerun()
        
        # Add feedback settings in sidebar
        if st.session_state.get("session"):
            st.header("Feedback Settings")
            feedback_settings()
    
    # Main content area
    if st.session_state.get("session"):
        st.header(f"{st.session_state.session['language']} Practice")
        
        # Chat container
        chat_container = st.container()
        with chat_container:
            # Display conversation history
            messages = get_conversation_history()
            if messages:
                chat_interface(messages)
            
            # Message input and controls
            msg = message_input()
            if msg:
                # Show spinner while processing message
                with st.spinner("Processing..."):
                    response_data = asyncio.run(handle_message(msg))
                    if response_data.get("response"):
                        st.rerun()
            
            # Conversation controls at the bottom
            st.markdown("---")  # Add separator
            control_action = conversation_controls()
            if control_action == "reset":
                # Clear session state for conversation
                if "session" in st.session_state:
                    del st.session_state.session
                st.rerun()
            elif control_action == "export":
                # TODO: Implement chat export
                st.info("Chat export coming soon!")
            elif control_action == "change_topic":
                new_topic = st.text_input("Enter new topic:", key="new_topic")
                if st.button("Set Topic"):
                    # Update the session topic
                    st.session_state.session["current_topic"] = new_topic
                    st.rerun()

if __name__ == "__main__":
    main()