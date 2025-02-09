"""
Exercise card component for grammar exercises.
"""
import streamlit as st
from typing import List, Optional, Callable

def create_grammar_exercise(
    prompt: str,
    exercise_type: str,
    options: Optional[List[str]] = None,
    correct_answer: str = "",
    on_submit: Optional[Callable[[str], None]] = None
) -> None:
    """
    Create an interactive grammar exercise card.
    
    Args:
        prompt: The exercise prompt or question
        exercise_type: Type of exercise ('fill_blanks' or 'multiple_choice')
        options: List of options for multiple choice questions
        correct_answer: The correct answer for validation
        on_submit: Callback function when answer is submitted
    """
    with st.container():
        st.write("---")
        st.subheader("Grammar Exercise")
        st.write(prompt)
        
        # Initialize session state for this exercise if not exists
        if "current_answer" not in st.session_state:
            st.session_state.current_answer = ""
        if "feedback_message" not in st.session_state:
            st.session_state.feedback_message = ""
            
        def check_answer():
            if st.session_state.current_answer.lower().strip() == correct_answer.lower().strip():
                st.session_state.feedback_message = "✅ Correct! Well done!"
            else:
                st.session_state.feedback_message = f"❌ Not quite. The correct answer is: {correct_answer}"
            if on_submit:
                on_submit(st.session_state.current_answer)
        
        if exercise_type == "fill_blanks":
            st.text_input(
                "Your answer:",
                key="current_answer",
                help="Type your answer here"
            )
            
        elif exercise_type == "multiple_choice":
            if options:
                st.radio(
                    "Select your answer:",
                    options,
                    key="current_answer",
                    help="Choose the correct option"
                )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("Submit", use_container_width=True):
                check_answer()
        with col2:
            if st.session_state.feedback_message:
                st.write(st.session_state.feedback_message)
        
        st.write("---")
