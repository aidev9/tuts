"""
Exercise card component for grammar exercises.
"""
import streamlit as st
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
                
                # Show radio button without default selection
                st.radio(
                    "Select your answer:",
                    options,
                    key="current_answer",
                    index=None,  # No default selection
                    help="Choose the correct option"
                )
        
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
