from pydantic_ai import Agent
from typing import Literal

class LanguageTutorAgent:
    def __init__(self):
        self.agent = Agent('ollama:llama3.2')
        self.current_language = None
        self.proficiency_level = None
        
    def set_language(self, language: str):
        """Set the target language for the session"""
        self.current_language = language
        return f"Language set to {language}"
        
    def set_proficiency(self, level: Literal[1, 2, 3, 4, 5]):
        """Set the user's proficiency level"""
        self.proficiency_level = level
        return f"Proficiency level set to {level}"
        
    def start_session(self, session_type: Literal["conversation", "vocabulary", "grammar"]):
        """Start a new learning session"""
        if not self.current_language or not self.proficiency_level:
            raise ValueError("Language and proficiency level must be set first")
            
        return {
            "session_type": session_type,
            "language": self.current_language,
            "level": self.proficiency_level,
            "status": "active"
        }
        
    def generate_conversation(self, topic: str = None):
        """Generate a conversation prompt"""
        prompt = f"Generate a {self.current_language} conversation at level {self.proficiency_level}"
        if topic:
            prompt += f" about {topic}"
        return self.agent.run_stream(prompt)
        
    def generate_vocabulary(self, topic: str = None):
        """Generate vocabulary words"""
        prompt = f"Generate {self.current_language} vocabulary at level {self.proficiency_level}"
        if topic:
            prompt += f" about {topic}"
        return self.agent.run_stream(prompt)
        
    def generate_grammar_exercise(self, exercise_type: Literal["fill_in_blank", "multiple_choice"]):
        """Generate a grammar exercise"""
        prompt = f"Generate a {self.current_language} grammar exercise at level {self.proficiency_level}"
        prompt += f" of type {exercise_type}"
        return self.agent.run_stream(prompt)