import random
from .base_agent import BaseLanguageTutorAgent
from models.schemas import UserSession
from typing import Dict, List
import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent

class FlashcardResponse(BaseModel):
    word: str
    translation: str
    example: str
    part_of_speech: str
    synonyms: List[str]
    antonyms: List[str]
    collocations: List[str]
    usage_notes: str

class VocabularyAgent(BaseLanguageTutorAgent):
    def _get_format_specific_prompt(self) -> str:
        proficiency_desc = {
            1: "beginner - focus on basic, high-frequency words",
            2: "elementary - common everyday vocabulary",
            3: "intermediate - broader vocabulary range",
            4: "advanced - sophisticated vocabulary",
            5: "fluent - nuanced and specialized terms"
        }[self.user_session.proficiency_level]

        topic_focus = f" related to {self.user_session.topic}" if self.user_session.topic else ""

        return (
            f"You are a vocabulary tutor teaching {self.user_session.language} vocabulary{topic_focus}. "
            f"The user's proficiency level is {proficiency_desc}.\n\n"
            f"Your role is to:\n"
            f"1. Introduce new vocabulary in context\n"
            f"2. Provide clear examples and usage patterns\n"
            f"3. Explain nuances and connotations\n"
            f"4. Show common collocations and phrases\n"
            f"5. Connect words to related vocabulary\n"
        )
    
    async def generate_flashcard(self) -> Dict:
        """Generate a vocabulary flashcard using the LLM"""
        # Define vocabulary categories
        categories = [
            "everyday activities and routines",
            "emotions and feelings",
            "food and dining",
            "travel and transportation",
            "work and professional life",
            "hobbies and leisure",
            "technology and modern life",
            "nature and environment",
            "social relationships",
            "arts and culture",
            "health and wellness",
            "home and living spaces"
        ]

        # Create a new agent for flashcard generation
        flashcard_agent = Agent(
            model=self.agent.model,
            result_type=FlashcardResponse,
            system_prompt=(
                f"You are a vocabulary teacher for {self.user_session.language} learners "
                f"at proficiency level {self.user_session.proficiency_level}.\n\n"
                
                f"Create rich vocabulary flashcards that include:\n"
                f"1. The target word in {self.user_session.language}\n"
                f"2. Its translation\n"
                f"3. A natural example sentence\n"
                f"4. Part of speech and usage information\n"
                f"5. Synonyms and antonyms\n"
                f"6. Common collocations\n"
                f"7. Important usage notes\n\n"
                
                f"Guidelines:\n"
                f"1. Choose words appropriate for level {self.user_session.proficiency_level}\n"
                f"2. Provide clear, practical examples\n"
                f"3. Include cultural context when relevant\n"
                f"4. Focus on high-value, frequently used vocabulary\n"
                f"5. NEVER repeat words that have been used before\n"
            )
        )

        # Select a category and create a focused prompt
        category = self.user_session.topic or random.choice(categories)
        prompt = (
            f"Generate a vocabulary flashcard for a word {category}.\n"
            f"Make sure it's appropriate for {self.user_session.language} learners "
            f"at level {self.user_session.proficiency_level}."
        )

        # Generate the flashcard
        result = await flashcard_agent.run(prompt)

        return {
            "word": result.data.word,
            "translation": result.data.translation,
            "usage_example": result.data.example,
            "part_of_speech": result.data.part_of_speech,
            "synonyms": ", ".join(result.data.synonyms),
            "antonyms": ", ".join(result.data.antonyms),
            "collocations": ", ".join(result.data.collocations),
            "usage_notes": result.data.usage_notes
        }
