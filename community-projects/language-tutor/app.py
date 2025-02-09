import streamlit as st
import asyncio
from pydantic_ai.models.groq import GroqModel
import os
from dotenv import load_dotenv

from models.schemas import UserSession, LearningFormat, GrammarFormat
from agents.conversation_agent import ConversationAgent
from agents.vocabulary_agent import VocabularyAgent
from agents.grammar_agent import GrammarAgent
from components.exercise_card import create_grammar_exercise
from components.flashcard import create_flashcard
from utils.exercise_generator import ExerciseGenerator

st.set_page_config(
    page_title="Language Tutor",
    page_icon="📚",
    layout="wide"
)

st.title("🌍 Interactive Language Tutor")
st.caption("Your personal AI language tutor")

# Initialize session state
if "session_initialized" not in st.session_state:
    st.session_state.session_initialized = False
    st.session_state.user_session = None
    st.session_state.exercise_generator = None
    st.session_state.current_exercise = None
    st.session_state.messages = []

# Session setup
if not st.session_state.session_initialized:
    with st.container():
        st.subheader("Let's set up your learning session! 🎯")
        
        col1, col2 = st.columns(2)
        
        with col1:
            language = st.selectbox(
                "What language would you like to learn?",
                ["English", "Spanish", "French", "German", "Italian", "Portuguese"],
                index=None,
                placeholder="Choose a language..."
            )
            
            proficiency = st.slider(
                "What's your current proficiency level?",
                min_value=1,
                max_value=5,
                value=1,
                help="1: Beginner, 5: Advanced"
            )
        
        with col2:
            format_type = st.selectbox(
                "What type of session would you like?",
                [format.value for format in LearningFormat],
                index=None,
                placeholder="Choose a session type..."
            )
            
            topic = None
            if format_type == LearningFormat.GRAMMAR.value:
                grammar_format = st.selectbox(
                    "What type of grammar practice would you like?",
                    [format.value for format in GrammarFormat],
                    index=None,
                    placeholder="Choose a grammar format..."
                )
            else:  # CONVERSATION or WORD_GAIN
                topic = st.text_input(
                    "What topic would you like to focus on?",
                    placeholder="e.g., Travel, Food, Business..."
                )

        if language and format_type:
            if st.button("Start Learning!", type="primary", use_container_width=True):
                # Initialize model
                load_dotenv()
                GROQ_API_KEY = os.getenv("GROQ_API_KEY")
                if not GROQ_API_KEY:
                    st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
                    st.stop()

                model = GroqModel(
                    model_name='llama-3.3-70b-versatile',
                    api_key=GROQ_API_KEY
                )

                # Create user session
                st.session_state.user_session = UserSession(
                    language=language,
                    proficiency_level=proficiency,
                    preferred_format=format_type,
                    topic=topic if format_type != LearningFormat.GRAMMAR.value else None,
                    grammar_format=grammar_format if format_type == LearningFormat.GRAMMAR.value else None
                )
                
                # Initialize exercise generator with appropriate format
                st.session_state.exercise_generator = ExerciseGenerator(
                    language=language,
                    proficiency_level=proficiency,
                    topic=topic if topic else "general vocabulary",
                    model=model
                )
                
                # Update grammar format if in grammar mode
                if format_type == LearningFormat.GRAMMAR.value and grammar_format:
                    grammar_session = st.session_state.exercise_generator.grammar_agent.user_session
                    grammar_session.grammar_format = grammar_format
                
                st.session_state.session_initialized = True
                st.rerun()


else:
    # Session info in sidebar
    st.sidebar.success(f"Learning {st.session_state.user_session.language} - Level {st.session_state.user_session.proficiency_level}")
    if st.sidebar.button("Start New Session", use_container_width=True):
        st.session_state.session_initialized = False
        st.session_state.user_session = None
        st.session_state.exercise_generator = None
        st.session_state.current_exercise = None
        st.session_state.messages = []
        st.rerun()
    
    # Main exercise area
    if st.session_state.user_session.preferred_format == LearningFormat.GRAMMAR.value:
        # Grammar exercises
        if not st.session_state.current_exercise:
            st.session_state.current_exercise = st.session_state.exercise_generator.generate_grammar_exercise(
                st.session_state.user_session.grammar_format.lower()
            )
        
        # Display current exercise
        def next_exercise():
            # Clear feedback before loading new exercise
            if "feedback_message" in st.session_state:
                del st.session_state.feedback_message
            
            st.session_state.current_exercise = st.session_state.exercise_generator.generate_grammar_exercise(
                st.session_state.user_session.grammar_format.lower()
            )
            st.rerun()
            
        create_grammar_exercise(
            prompt=st.session_state.current_exercise["prompt"],
            exercise_type=st.session_state.current_exercise["exercise_type"],
            content=st.session_state.current_exercise["content"],
            correct_answer=st.session_state.current_exercise["correct_answer"],
            explanation=st.session_state.current_exercise["explanation"],
            options=st.session_state.current_exercise.get("options"),
            on_next=next_exercise
        )
            
    elif st.session_state.user_session.preferred_format == LearningFormat.WORD_GAIN.value:
        # Vocabulary flashcards
        if not st.session_state.current_exercise:
            st.session_state.current_exercise = st.session_state.exercise_generator.generate_vocabulary_card()
        
        def next_card():
            st.session_state.current_exercise = st.session_state.exercise_generator.generate_vocabulary_card()
            st.rerun()
        
        # Display current flashcard
        create_flashcard(
            word=st.session_state.current_exercise["word"],
            translation=st.session_state.current_exercise["translation"],
            usage_example=st.session_state.current_exercise["usage_example"],
            on_next=next_card
        )
        
    else:  # Conversation mode
        if "agent" not in st.session_state:
            # Initialize model if not already done
            load_dotenv()
            GROQ_API_KEY = os.getenv("GROQ_API_KEY")
            if not GROQ_API_KEY:
                st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
                st.stop()

            model = GroqModel(
                model_name='llama-3.3-70b-versatile',
                api_key=GROQ_API_KEY
            )
            
            st.session_state.agent = ConversationAgent(model, st.session_state.user_session)
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "corrections" in message and message["corrections"]:
                    st.markdown("---")
                    st.markdown(f"🎯 **Corrections & Suggestions:**\n{message['corrections']}")

        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            try:
                with st.spinner(f"Your tutor is thinking..."):
                    response = asyncio.run(st.session_state.agent.process_message(prompt, st.session_state.messages))
                    
                    message = {
                        "role": "assistant",
                        "content": response.content,
                        "corrections": response.corrections if response.corrections else ""
                    }
                    st.session_state.messages.append(message)

                    with st.chat_message("assistant"):
                        st.markdown(response.content)
                        if response.corrections:
                            st.markdown("---")
                            st.markdown(f"🎯 **Corrections & Suggestions:**\n{response.corrections}")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")