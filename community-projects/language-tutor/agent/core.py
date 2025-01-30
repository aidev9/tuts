from pydantic_ai import Agent
from typing import Literal, Optional, Dict, Any
import asyncio
from data import get_db, ConversationRepository
import json

class LanguageTutorAgent:
    def __init__(self):
        self.agent = Agent('ollama:llama3.2')
        self.current_language = None
        self.proficiency_level = None
        self._session_id = None
        
    def set_language(self, language: str):
        """Set the target language for the session"""
        self.current_language = language
        with get_db() as db:
            repo = ConversationRepository(db)
            if self._session_id:
                repo.update_session_state(self._session_id, language=language)
        return f"Language set to {language}"
        
    def set_proficiency(self, level: Literal[1, 2, 3, 4, 5]):
        """Set the user's proficiency level"""
        self.proficiency_level = level
        with get_db() as db:
            repo = ConversationRepository(db)
            if self._session_id:
                repo.update_session_state(self._session_id, proficiency_level=level)
        return f"Proficiency level set to {level}"
        
    def start_session(self, session_type: Literal["conversation", "vocabulary", "grammar"]):
        """Start a new learning session"""
        if not self.current_language or not self.proficiency_level:
            raise ValueError("Language and proficiency level must be set first")
            
        with get_db() as db:
            repo = ConversationRepository(db)
            session = repo.get_current_session()
            if not session:
                # Create new session state
                from data.database import get_or_create_session_state
                session = get_or_create_session_state(
                    db, 
                    self.current_language, 
                    self.proficiency_level
                )
            self._session_id = session.id
            
        return {
            "session_type": session_type,
            "language": self.current_language,
            "level": self.proficiency_level,
            "status": "active"
        }
        
    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process a user message and return response with feedback"""
        if not self._session_id:
            return {
                "response": "Please start a session first.",
                "corrections": None
            }
        
        with get_db() as db:
            repo = ConversationRepository(db)
            
            # Store user message
            repo.create_message(
                conversation_id=self._session_id,
                role="user",
                content=message
            )
            
            # Generate response and corrections
            response, corrections = self._generate_response(message)
            
            # Store assistant response
            repo.create_message(
                conversation_id=self._session_id,
                role="assistant",
                content=response,
                corrections=corrections
            )
            
            return {
                "response": response,
                "corrections": corrections
            }
            
    def _generate_response(self, message: str) -> tuple[str, Optional[Dict]]:
        """Generate a response and corrections for the user's message"""
        # TODO: Implement actual NLP/AI processing here
        # For now, return a simple response
        corrections = None
        
        # Simple correction example
        if "wetin" in message.lower():
            corrections = {
                "grammar": [
                    "Consider using 'what is' instead of 'wetin'"
                ],
                "vocabulary": [
                    "'wetin' is informal pidgin English. In standard English, use 'what is happening' or 'what's happening'"
                ]
            }
            response = "I notice you're using pidgin English. Would you like to practice standard English instead? What's happening with you today?"
        else:
            response = f"I understand you're trying to communicate in {self.current_language}. Please continue, and I'll help you improve!"
        
        return response, corrections
        
    def _create_response_prompt(self, message: str) -> str:
        """Create a prompt for generating responses"""
        return f"""
        You are a language tutor helping someone learn {self.current_language}.
        Their proficiency level is {self.proficiency_level} out of 5.
        
        Analyze their message and respond appropriately in {self.current_language}.
        Also provide corrections and suggestions if needed.
        
        User message: {message}
        
        Return your response in JSON format:
        {{
            "response": "Your response in {self.current_language}",
            "corrections": {{
                "grammar": ["any grammar corrections"],
                "vocabulary": ["any vocabulary suggestions"],
                "pronunciation": ["any pronunciation tips"]
            }}
        }}
        """
        
    async def generate_conversation(self, topic: str = None):
        """Generate a conversation prompt"""
        prompt = f"Generate a {self.current_language} conversation at level {self.proficiency_level}"
        if topic:
            prompt += f" about {topic}"
        async with self.agent.run_stream(prompt) as result:
            return await result.get_data()
        
    async def generate_vocabulary(self, topic: str = None):
        """Generate vocabulary words"""
        prompt = f"Generate {self.current_language} vocabulary at level {self.proficiency_level}"
        if topic:
            prompt += f" about {topic}"
        async with self.agent.run_stream(prompt) as result:
            return await result.get_data()
        
    async def generate_grammar_exercise(self, exercise_type: Literal["fill_in_blank", "multiple_choice"]):
        """Generate a grammar exercise"""
        prompt = f"Generate a {self.current_language} grammar exercise at level {self.proficiency_level}"
        prompt += f" of type {exercise_type}"
        async with self.agent.run_stream(prompt) as result:
            return await result.get_data()