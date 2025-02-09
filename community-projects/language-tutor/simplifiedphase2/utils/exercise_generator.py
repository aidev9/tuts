"""
Utility functions for generating exercises and managing exercise state.
"""
from typing import List, Dict, Tuple, Optional
import random
import asyncio
from pydantic_ai.models.groq import GroqModel
from models.schemas import UserSession
from agents.vocabulary_agent import VocabularyAgent

class ExerciseGenerator:
    def __init__(self, language: str, proficiency_level: int, topic: str, model: Optional[GroqModel] = None):
        self.language = language
        self.proficiency_level = proficiency_level
        self.topic = topic
        self.model = model
        
        if model:
            # Create user session for agents
            self.user_session = UserSession(
                language=language,
                proficiency_level=proficiency_level,
                topic=topic,
                preferred_format="word_gain"  # Set to word_gain since this is for vocabulary
            )
            # Initialize vocabulary agent
            self.vocabulary_agent = VocabularyAgent(model, self.user_session)
        
    def generate_grammar_exercise(self, exercise_type: str) -> Dict:
        """
        Generate a grammar exercise based on type and proficiency.
        This is a simplified version - in practice, this would use the LLM
        to generate more contextual exercises.
        """
        if exercise_type == "fill_blanks":
            return {
                "prompt": "Complete the sentence with the correct form:",
                "exercise_type": "fill_blanks",
                "correct_answer": "am learning",
                "content": "I _____ the " + self.language + " language."
            }
        else:  # multiple_choice
            return {
                "prompt": "Choose the correct form:",
                "exercise_type": "multiple_choice",
                "options": ["am learning", "learning", "learn", "learns"],
                "correct_answer": "am learning",
                "content": "I _____ the " + self.language + " language."
            }
            
    def generate_vocabulary_card(self) -> Dict:
        """
        Generate a vocabulary flashcard using the LLM if available,
        otherwise fall back to basic examples.
        """
        if self.model and hasattr(self, 'vocabulary_agent'):
            # Use LLM to generate flashcard
            flashcard = asyncio.run(self.vocabulary_agent.generate_flashcard())
            return {
                "word": flashcard.word,
                "translation": flashcard.translation,
                "usage_example": flashcard.example
            }
        
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
