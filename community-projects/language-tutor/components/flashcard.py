"""
Flashcard component for vocabulary learning.
"""
import streamlit as st
from typing import Optional, Callable

def create_flashcard(
    word: str,
    translation: str,
    usage_example: Optional[str] = None,
    on_next: Optional[Callable[[], None]] = None
) -> None:
    """
    Create an interactive vocabulary flashcard.
    
    Args:
        word: The word or phrase to learn
        translation: The translation of the word
        usage_example: Optional example sentence using the word
        on_next: Callback function when moving to next card
    """
    with st.container():
        st.write("---")
        st.subheader("📝 Vocabulary Flashcard")
        
        # Initialize session state for this flashcard
        if "show_translation" not in st.session_state:
            st.session_state.show_translation = False
        if "show_example" not in st.session_state:
            st.session_state.show_example = False
        if "practice_mode" not in st.session_state:
            st.session_state.practice_mode = False
            
        # Word display
        with st.expander("🔤 Word/Phrase", expanded=True):
            st.header(word)
            st.caption("Click the buttons below to reveal more information")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔍 Show Translation", use_container_width=True):
                st.session_state.show_translation = True
                st.session_state.practice_mode = False
                
        with col2:
            if usage_example and st.button("📖 Show Example", use_container_width=True):
                st.session_state.show_example = True
                st.session_state.practice_mode = False
                
        with col3:
            if st.button("✍️ Practice", use_container_width=True):
                st.session_state.practice_mode = True
                st.session_state.show_translation = False
                st.session_state.show_example = False
        
        # Show translation if requested
        if st.session_state.show_translation:
            with st.expander("🌍 Translation", expanded=True):
                st.info(translation)
            
        # Show example if available and requested
        if usage_example and st.session_state.show_example:
            with st.expander("📝 Example Usage", expanded=True):
                st.write(usage_example)
            
        # Practice mode
        if st.session_state.practice_mode:
            with st.expander("🎯 Practice Mode", expanded=True):
                # Initialize practice state
                if "practice_answer" not in st.session_state:
                    st.session_state.practice_answer = ""
                if "practice_feedback" not in st.session_state:
                    st.session_state.practice_feedback = ""
                    
                st.text_input(
                    "Type the translation of the word/phrase above:",
                    key="practice_answer",
                    help="Type your answer and click Check"
                )
                
                def normalize_text(text: str) -> str:
                    """Normalize text for comparison by removing extra spaces and articles"""
                    # Convert to lowercase and remove extra whitespace
                    text = " ".join(text.lower().split())
                    
                    # Remove common articles and punctuation
                    articles = ["a", "an", "the"]
                    words = text.split()
                    words = [w for w in words if w not in articles]
                    text = " ".join(words)
                    
                    # Remove punctuation except hyphens between words
                    text = "".join(c for c in text if c.isalnum() or c.isspace() or c == '-')
                    
                    return text.strip()
                
                def check_practice():
                    user_answer = normalize_text(st.session_state.practice_answer)
                    correct_answer = normalize_text(translation)
                    
                    # Check if answers match after normalization
                    if user_answer == correct_answer:
                        st.session_state.practice_feedback = "✅ Correct! Well done!"
                    else:
                        # Calculate similarity (basic word overlap)
                        user_words = set(user_answer.split())
                        correct_words = set(correct_answer.split())
                        common_words = user_words & correct_words
                        
                        # If most words match (>70%), consider it mostly correct
                        if len(common_words) / max(len(user_words), len(correct_words)) > 0.7:
                            st.session_state.practice_feedback = (
                                f"✅ Almost perfect! Your answer captures the meaning.\n\n"
                                f"Your answer: {st.session_state.practice_answer}\n"
                                f"Model answer: {translation}"
                            )
                        else:
                            st.session_state.practice_feedback = (
                                f"❌ Not quite right.\n\n"
                                f"Your answer: {st.session_state.practice_answer}\n"
                                f"Model answer: {translation}"
                            )
                
                if st.button("Check Answer", use_container_width=True):
                    check_practice()
                
                if st.session_state.practice_feedback:
                    if "✅" in st.session_state.practice_feedback:
                        st.success(st.session_state.practice_feedback)
                    else:
                        st.error(st.session_state.practice_feedback)
        
        st.write("---")
        
        # Next card button
        if on_next:
            col1, col2 = st.columns([4, 1])
            with col2:
                if st.button("Next Card →", use_container_width=True):
                    # Reset states
                    st.session_state.show_translation = False
                    st.session_state.show_example = False
                    st.session_state.practice_mode = False
                    if "practice_answer" in st.session_state:
                        del st.session_state.practice_answer
                    if "practice_feedback" in st.session_state:
                        del st.session_state.practice_feedback
                    # Call next callback
                    on_next()
                    # Force a rerun to reset the widget states
                    st.rerun()
