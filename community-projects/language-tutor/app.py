import streamlit as st
from dotenv import load_dotenv
from agent import LanguageTutorAgent
from ui.components import (
    language_selector,
    proficiency_slider,
    session_type_selector,
    topic_input,
    grammar_format_selector
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
        
        if st.button("Start Session"):
            st.session_state.agent.set_language(language)
            st.session_state.agent.set_proficiency(level)
            session = st.session_state.agent.start_session(session_type)
            st.session_state.session = session
            st.success(f"Started {session_type} session in {language} at level {level}")
    
    # Main content area
    if st.session_state.get("session"):
        st.header(f"{st.session_state.session['language']} Practice")
        
        if st.session_state.session["session_type"] == "conversation":
            if topic:
                st.write(st.session_state.agent.generate_conversation(topic))
            else:
                st.write(st.session_state.agent.generate_conversation())
                
        elif st.session_state.session["session_type"] == "vocabulary":
            if topic:
                st.write(st.session_state.agent.generate_vocabulary(topic))
            else:
                st.write(st.session_state.agent.generate_vocabulary())
                
        elif st.session_state.session["session_type"] == "grammar":
            st.write(st.session_state.agent.generate_grammar_exercise(grammar_format))

if __name__ == "__main__":
    main()