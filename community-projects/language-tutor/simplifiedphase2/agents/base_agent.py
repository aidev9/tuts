from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel
from typing import Optional
from models.schemas import UserSession, LearningFormat, GrammarFormat

class AgentResponse(BaseModel):
    content: str
    corrections: Optional[str] = None
    suggestions: Optional[str] = None

class BaseLanguageTutorAgent:
    def __init__(self, model: GroqModel, user_session: UserSession):
        self.user_session = user_session
        self.agent = Agent(
            model=model,
            result_type=AgentResponse,
            system_prompt=self._get_system_prompt()
        )
    
    def _get_system_prompt(self) -> str:
        base_prompt = (
            f"You are a language tutor helping someone learn {self.user_session.language}. "
            f"Their proficiency level is {self.user_session.proficiency_level} out of 5.\n\n"
        )
        
        format_specific = self._get_format_specific_prompt()
        return base_prompt + format_specific
    
    def _get_format_specific_prompt(self) -> str:
        """Override this method in specific agent implementations"""
        return ""
    
    async def process_message(self, message: str) -> AgentResponse:
        """Process a user message and return a response"""
        result = await self.agent.run(message)
        return result.data
