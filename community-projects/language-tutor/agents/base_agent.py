from pydantic_ai import Agent
from pydantic_ai.models.groq import GroqModel
from pydantic import BaseModel
from typing import Optional, List, Dict
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
        self.conversation_history: List[Dict[str, str]] = []
    
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
    
    def _format_conversation_history(self) -> str:
        """Format conversation history for the model"""
        if not self.conversation_history:
            return ""
            
        history = "Previous conversation:\n"
        for msg in self.conversation_history:
            if msg["role"] == "user":
                history += f"User: {msg['content']}\n"
            else:
                history += f"Assistant: {msg['content']}\n"
                if msg.get("corrections"):
                    history += f"Corrections: {msg['corrections']}\n"
        return history + "\nCurrent conversation:\n"
    
    async def process_message(self, message: str, messages: Optional[List[Dict[str, str]]] = None) -> AgentResponse:
        """Process a user message and return a response"""
        # Update conversation history
        if messages:
            self.conversation_history = messages[:-1]  # Exclude current message
        
        # Prepare context with history
        context = self._format_conversation_history() + message
        
        # Get response from model
        result = await self.agent.run(context)
        return result.data
