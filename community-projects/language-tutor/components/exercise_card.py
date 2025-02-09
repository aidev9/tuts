"""
Exercise card component for grammar exercises.
"""
import streamlit as st
import random
from typing import List, Optional, Callable, Tuple
from unidecode import unidecode

def create_grammar_exercise(
    prompt: str,
    exercise_type: str,
    content: str,
    correct_answer: str,
    explanation: str,
    options: Optional[List[str]] = None,
    on_next: Optional[Callable[[], None]] = None
) -> None:
    """
    Create an interactive grammar exercise card.
    
    Args:
        prompt: The exercise prompt/instruction
        exercise_type: Type of exercise ('fill_blanks' or 'multiple_choice')
        content: The exercise content with blanks
        correct_answer: The correct answer
        explanation: Grammar explanation for the exercise
        options: List of options for multiple choice
        on_next: Callback function when moving to next exercise
    """
    with st.container():
        st.write("---")
        st.subheader("📚 Grammar Exercise")
        
        # Initialize session state
        if "current_answer" not in st.session_state:
            st.session_state.current_answer = ""
        if "feedback_message" not in st.session_state:
            st.session_state.feedback_message = ""
            
        # Display prompt and content in an expander
        with st.expander("❓ Exercise", expanded=True):
            st.write(prompt)
            st.markdown(f"**{content}**")
        
        # Input based on exercise type
        col1, col2 = st.columns([3, 1])
        with col1:
            if exercise_type == "fill_blanks":
                st.text_input(
                    "Your answer:",
                    key="current_answer",
                    help="Type your answer and click Check"
                )
            else:  # multiple_choice
                # Ensure we have options for multiple choice
                if not options:
                    st.error("No options provided for multiple choice question!")
                    return

                # Initialize options in session state
                if "current_options" not in st.session_state:
                    shuffled = list(options)
                    random.shuffle(shuffled)
                    st.session_state.current_options = shuffled
                
                # Show radio button without default selection
                answer =st.radio(
                    "Select your answer:",
                    st.session_state.current_options,
                    key="answer_radio",
                    index=None,  # No default selection
                    help="Choose the correct option"
                )

                # Update current answer with selected option
                st.session_state.current_answer = answer if answer else ""
        
        with col2:
            def compare_answers(user_input: str, correct: str) -> Tuple[bool, bool, str, str]:
                """Compare answers with and without accents.
                Returns: (exact_match, close_match, normalized_user, normalized_correct)"""
                # Clean and normalize both answers
                user_clean = user_input.lower().strip()
                correct_clean = correct.lower().strip()
                
                # Remove accents for comparison
                user_no_accents = unidecode(user_clean)
                correct_no_accents = unidecode(correct_clean)
                
                return (
                    user_clean == correct_clean,  # Exact match
                    user_no_accents == correct_no_accents,  # Close match (ignoring accents)
                    user_clean,
                    correct_clean
                )
            
            # Check answer button
            if st.button("✅ Check Answer", use_container_width=True):
                exact_match, close_match, user_norm, correct_norm = compare_answers(
                    st.session_state.current_answer,
                    correct_answer
                )
                
                if exact_match:
                    st.session_state.feedback_message = (
                        "✅ Correct! Well done!\n\n"
                        f"Let's understand why:\n{explanation}"
                    )
                elif close_match:
                    st.session_state.feedback_message = (
                        "✅ Almost perfect!\n\n"
                        f"Your answer '{user_norm}' is correct, but remember to use the proper accents: '{correct_norm}'\n\n"
                        f"Let's understand the grammar:\n{explanation}"
                    )
                else:
                    st.session_state.feedback_message = (
                        f"❌ Not quite right.\n\n"
                        f"Your answer: {user_norm}\n"
                        f"Correct answer: {correct_norm}\n\n"
                        f"Explanation:\n{explanation}"
                    )
                
        # Display feedback in an expander if there is any
        if st.session_state.feedback_message:
            with st.expander("📘 Feedback & Explanation", expanded=True):
                if "✅" in st.session_state.feedback_message:
                    st.success(st.session_state.feedback_message)
                else:
                    st.error(st.session_state.feedback_message)
            
        st.write("---")
        
        # Next exercise button
        col1, col2 = st.columns([4, 1])
        with col2:
            if on_next and st.button("Next Exercise →", use_container_width=True):
                # Reset states and trigger next exercise
                on_next()
                # Force a rerun to properly reset widget states
                st.rerun()

def create_vocabulary_flashcard(
    word: str,
    translation: str,
    usage_example: str,
    part_of_speech: str = "",
    synonyms: str = "",
    antonyms: str = "",
    collocations: str = "",
    usage_notes: str = "",
    on_next: Optional[Callable[[], None]] = None
) -> None:
    """Create an interactive vocabulary flashcard with rich context.
    
    Args:
        word: The word in the target language
        translation: The English translation
        usage_example: Example sentence using the word
        part_of_speech: The word's part of speech
        synonyms: List of synonyms
        antonyms: List of antonyms
        collocations: Common word combinations
        usage_notes: Additional usage information
        on_next: Callback function when moving to next card
    """
    with st.container():
        st.write("---")
        st.subheader("📚 Vocabulary Flashcard")
        
        # Main word and translation
        col1, col2 = st.columns([2, 3])
        with col1:
            st.markdown(f"### {word}")
            if part_of_speech:
                st.caption(f"*{part_of_speech}*")
        with col2:
            st.markdown(f"**Translation:** {translation}")
        
        # Example usage
        with st.expander("📝 Example Usage", expanded=True):
            st.markdown(f"*{usage_example}*")
        
        # Additional information in tabs
        if any([synonyms, antonyms, collocations, usage_notes]):
            tab1, tab2, tab3, tab4 = st.tabs(["Synonyms", "Antonyms", "Collocations", "Usage Notes"])
            
            with tab1:
                if synonyms:
                    st.markdown(f"**Similar words:** {synonyms}")
                else:
                    st.caption("No synonyms available")
                    
            with tab2:
                if antonyms:
                    st.markdown(f"**Opposite words:** {antonyms}")
                else:
                    st.caption("No antonyms available")
                    
            with tab3:
                if collocations:
                    st.markdown(f"**Common combinations:** {collocations}")
                else:
                    st.caption("No collocations available")
                    
            with tab4:
                if usage_notes:
                    st.markdown(f"**Notes:** {usage_notes}")
                else:
                    st.caption("No additional notes available")
        
        st.write("---")
        
        # Next flashcard button
        col1, col2 = st.columns([4, 1])
        with col2:
            if on_next and st.button("Next Word →", use_container_width=True):
                on_next()
                st.rerun()
