from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class LearningFormat(str, Enum):
    CONVERSATION = "conversation"
    WORD_GAIN = "word_gain"
    GRAMMAR = "grammar"

class GrammarFormat(str, Enum):
    FILL_BLANKS = "fill_blanks"
    MULTIPLE_CHOICE = "multiple_choice"

class UserSession(BaseModel):
    language: str
    proficiency_level: int = Field(..., ge=1, le=5)
    preferred_format: LearningFormat
    topic: Optional[str] = None
    grammar_format: Optional[GrammarFormat] = None

    class Config:
        use_enum_values = True

class SessionConfig(BaseModel):
    format: LearningFormat
    topic: Optional[str] = None
    grammar_format: Optional[GrammarFormat] = None
    
    class Config:
        use_enum_values = True

class ProgressUpdate(BaseModel):
    session_id: int
    score: Optional[int] = None
    notes: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        use_enum_values = True
