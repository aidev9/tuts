from .base_agent import BaseLanguageTutorAgent
from models.schemas import UserSession
from typing import Dict
import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent

class FlashcardResponse(BaseModel):
    word: str
    translation: str
    example: str

class VocabularyAgent(BaseLanguageTutorAgent):
    def _get_format_specific_prompt(self) -> str:
        proficiency_desc = {
            1: "beginner - focus on basic, everyday vocabulary",
            2: "elementary - introduce common expressions and phrases",
            3: "intermediate - explore more nuanced vocabulary and idioms",
            4: "advanced - use sophisticated vocabulary and colloquialisms",
            5: "fluent - master specialized terminology and subtle nuances"
        }[self.user_session.proficiency_level]

        return (
            f"You are a vocabulary tutor helping with '{self.user_session.topic}' vocabulary in {self.user_session.language}. "
            f"The user's proficiency level is {proficiency_desc}.\n\n"
            f"Your role is to:\n"
            f"1. Introduce new vocabulary related to {self.user_session.topic}\n"
            f"2. Provide example sentences using the vocabulary\n"
            f"3. Ask the user to create their own sentences\n"
            f"4. Check their usage and provide corrections\n"
            f"5. Reinforce learning through context and practice\n\n"
            f"In each response:\n"
            f"- Present 2-3 new words/phrases at a time\n"
            f"- Include pronunciation hints if relevant\n"
            f"- Show example usage in natural contexts\n\n"
            f"Format your response as:\n"
            f"content: Your response in {self.user_session.language} (and English for new vocabulary)\n"
            f"corrections: Corrections and explanations for user mistakes (in English)\n\n"
            f"If introducing new vocabulary, format it as:\n"
            f"Word/Phrase: [original] - [meaning in English]\n"
            f"Example: [example sentence] - [translation]\n\n"
            f"If the user's usage is correct, leave the corrections field empty."
        )
    
    async def generate_flashcard(self) -> FlashcardResponse:
        """Generate a vocabulary flashcard using the LLM"""
        # Create a new agent specifically for flashcard generation
        flashcard_agent = Agent(
            model=self.agent.model,
            result_type=FlashcardResponse,
            system_prompt=(
                f"You are a vocabulary tutor generating flashcards for a {self.user_session.language} learner "
                f"studying the topic: {self.user_session.topic}. "
                f"Their proficiency level is {self.user_session.proficiency_level} out of 5.\n\n"
                f"Generate a flashcard with:\n"
                f"1. A word or phrase in {self.user_session.language} appropriate for their level"
                f"2. Its English translation (clear and concise)"
                f"3. A natural example sentence using the word/phrase in {self.user_session.language}\n"
                f"Return the flashcard in JSON format with these exact fields:\n"
                f"- word: the word/phrase in {self.user_session.language}\n"
                f"- translation: the English translation\n"
                f"- example: example sentence in {self.user_session.language}"
            )
        )
        
        # Generate the flashcard
        result = await flashcard_agent.run("Generate a flashcard")
        return result.data
