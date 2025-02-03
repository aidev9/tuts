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
import logging

# Create a logger
logger = logging.getLogger(__name__)

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

async def handle_message(message: str) -> None:
    """Handle user message and get response"""
    try:
        # Process the message through the agent
        response = await st.session_state.agent.process_message(message)

        if not response.get("response"):
            return {"error": "No response received from the agent"}

        return response

    except Exception as e:
        logger.exception("Request handling failed")
        print(f"Error details: {str(e)}")  # For debugging
        return {"error": str(e)}

def get_conversation_history():
    """Get conversation history from database"""
    with get_db() as db:
        repo = ConversationRepository(db)
        if hasattr(st.session_state.agent, '_session_id'):
            messages = repo.get_conversation_history(st.session_state.agent._session_id)
            # Reverse the messages to show oldest first
            return list(reversed(messages))
    return []

async def process_and_display_response(msg):
    """Process the message and display the response in the UI."""
    with st.spinner("Processing..."):
        response_data = await handle_message(msg)
        if "error" in response_data:
            st.error(response_data["error"])
            return

        if response_data.get("response"):
            # The messages will be shown through chat_interface after rerun
            pass


async def main():
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
            message = message_input()

            if message:
                # Show the user message immediately
                st.chat_message("user").write(message)
                response_data = await handle_message(message)
                st.rerun()  # Remove this line

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
    asyncio.run(main())
