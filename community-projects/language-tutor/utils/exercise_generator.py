"""
Utility functions for generating exercises and managing exercise state.
"""
from typing import List, Dict, Tuple, Optional
import random
import asyncio
from pydantic_ai.models.groq import GroqModel
from models.schemas import UserSession, LearningFormat, GrammarFormat
from agents.vocabulary_agent import VocabularyAgent
from agents.grammar_agent import GrammarAgent

class ExerciseGenerator:
    def __init__(self, language: str, proficiency_level: int, topic: str, model: Optional[GroqModel] = None):
        self.language = language
        self.proficiency_level = proficiency_level
        self.topic = topic
        self.model = model
        
        if model:
            # Create base user session
            self.base_session = UserSession(
                language=language,
                proficiency_level=proficiency_level,
                topic=topic,
                preferred_format=LearningFormat.WORD_GAIN.value,  # Default format
                grammar_format=GrammarFormat.FILL_BLANKS.value  # Default grammar format
            )
            
            # Initialize vocabulary agent
            vocab_session = self.base_session.model_copy()
            vocab_session.preferred_format = LearningFormat.WORD_GAIN.value
            self.vocabulary_agent = VocabularyAgent(model, vocab_session)
            
            # Initialize grammar agent
            grammar_session = self.base_session.model_copy()
            grammar_session.preferred_format = LearningFormat.GRAMMAR.value
            grammar_session.grammar_format = GrammarFormat.FILL_BLANKS.value  # Set default grammar format
            self.grammar_agent = GrammarAgent(model, grammar_session)
        
    def generate_grammar_exercise(self, exercise_type: str) -> Dict:
        """
        Generate a grammar exercise based on type and proficiency.
        Uses the LLM if available, otherwise falls back to basic examples.
        """
        if self.model and hasattr(self, 'grammar_agent'):
            # Use LLM to generate exercise
            exercise = asyncio.run(self.grammar_agent.generate_exercise(exercise_type))
            return {
                "prompt": exercise.prompt,
                "exercise_type": exercise.exercise_type,
                "content": exercise.content,
                "correct_answer": exercise.correct_answer,
                "options": exercise.options if exercise.options else None,
                "explanation": exercise.explanation
            }
        
        # Fallback to basic examples if no LLM available
        if exercise_type == "fill_blanks":
            return {
                "prompt": "Complete the sentence with the correct form:",
                "exercise_type": "fill_blanks",
                "correct_answer": "am learning",
                "content": "I _____ the " + self.language + " language.",
                "explanation": "Use present continuous (am/is/are + -ing) for actions happening now."
            }
        else:  # multiple_choice
            return {
                "prompt": "Choose the correct form:",
                "exercise_type": "multiple_choice",
                "options": ["am learning", "learning", "learn", "learns"],
                "correct_answer": "am learning",
                "content": "I _____ the " + self.language + " language.",
                "explanation": "Use present continuous (am/is/are + -ing) for actions happening now."
            }
            
    def generate_vocabulary_card(self) -> Dict:
        """
        Generate a vocabulary flashcard using the LLM if available,
        otherwise fall back to basic examples.
        """
        if self.model and hasattr(self, 'vocabulary_agent'):
            # Use LLM to generate flashcard
            flashcard = asyncio.run(self.vocabulary_agent.generate_flashcard())
            return flashcard  # Return the full flashcard dictionary with all fields
        
        # Fallback to basic examples if no LLM available
        words = {
            "hello": {
                "translation": "hola" if self.language == "Spanish" else "bonjour",
                "example": "Hello, how are you today?"
            },
            "goodbye": {
                "translation": "adiós" if self.language == "Spanish" else "au revoir",
                "example": "Goodbye, see you tomorrow!"
            }
        }
        
        word = random.choice(list(words.keys()))
        return {
            "word": word,
            "translation": words[word]["translation"],
            "usage_example": words[word]["example"]
        }
