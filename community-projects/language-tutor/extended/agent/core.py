from pydantic_ai import Agent
from pydantic import BaseModel
from pydantic_ai.models.ollama import OllamaModel
from typing import Literal, Optional, Dict, Any
import asyncio
from data import get_db, ConversationRepository
import json
import logging

class AIResponse(BaseModel):
    content: str
    corrections: str

class LanguageTutorAgent:
    def __init__(self):
        self.agent = Agent(
            model=OllamaModel(
                model_name='llama3.2'
            ),
            result_type=AIResponse
        )
        self.ai_response = AIResponse(
            content="",
            corrections=""
        )
        self.current_language = None
        self.proficiency_level = None
        self._session_id = None
        self.logger = logging.getLogger(__name__)

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
            response, corrections = await self._generate_response(message)

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

    async def _generate_response(self, message: str) -> tuple[str, Optional[Dict]]:
        """Generate a response and corrections for the user's message"""
        prompt = self._create_response_prompt(message)
        try:
            # Use the context manager pattern for the stream
            async with self.agent.run_stream(prompt) as response_stream:
                response_text = await response_stream.get_data()

                try:
                    # Parse the JSON response
                    response_data = json.loads(response_text)
                    response = response_data.get("response")
                    corrections = response_data.get("corrections")

                    if not response:  # If response is empty or None
                        return "I'm having trouble generating a proper response.", None

                    return response, corrections

                except json.JSONDecodeError as e:
                    print(f"JSON decode error: {e}")
                    print(f"Raw response: {response_text}")
                    return "I'm having trouble understanding that. Please try again.", None

        except Exception as e:
            print(f"Error generating response: {e}")
            return "I encountered an error processing your request.", None

    def _create_response_prompt(self, message: str) -> str:
        """Create a prompt for generating responses"""
        return f"""
        You are a language tutor helping someone learn {self.current_language}.
        Their proficiency level is {self.proficiency_level} out of 5.

        Analyze their message and respond appropriately in {self.current_language}.
        Also provide corrections and suggestions if needed.

        Please respond to this message: {message}

        Your response must be in valid JSON format with this exact structure:
        {{
            "response": "<your response in {self.current_language}>",
            "corrections": {{
                "grammar": ["list of grammar corrections"],
                "vocabulary": ["list of vocabulary suggestions"],
                "pronunciation": ["list of pronunciation tips"]
            }}
        }}

        Important: Ensure your entire response is valid JSON and includes both the response and corrections fields.
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

    async def process_request(self, input_text: str) -> dict:
        """Return structured response format"""
        from datetime import datetime
        try:
            prompt = self._create_response_prompt(input_text)
            async with self.agent.run_stream(prompt) as response_stream:
                raw_response = await response_stream.get_data()
                try:
                    # Try to parse as JSON first
                    if isinstance(raw_response, str):
                        response_data = json.loads(raw_response)
                    else:
                        response_data = raw_response
                    
                    # Ensure the response has the expected structure
                    if not isinstance(response_data, dict):
                        raise ValueError("Response is not a dictionary")
                        
                    return {
                        "response": response_data.get("response", ""),
                        "corrections": response_data.get("corrections", {}),
                        "timestamp": datetime.now().isoformat(),
                        "session_id": self._session_id
                    }
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON response: {e}")
                    # If JSON parsing fails, return the raw response
                    return {
                        "response": raw_response,
                        "timestamp": datetime.now().isoformat(),
                        "session_id": self._session_id
                    }
        except ConnectionError as e:
            self.logger.error(f"API connection failed: {str(e)}")
            return {"error": "Connection error", "details": str(e)}
        except TimeoutError:
            self.logger.error("Model request timed out")
            return {"error": "Request timeout"}
        except Exception as e:
            self.logger.exception("Unexpected error processing request")
            return {"error": "Unexpected error", "details": str(e)}
