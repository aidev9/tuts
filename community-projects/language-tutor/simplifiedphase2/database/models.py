from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class LearningFormat(enum.Enum):
    CONVERSATION = "conversation"
    WORD_GAIN = "word_gain"
    GRAMMAR = "grammar"

class GrammarFormat(enum.Enum):
    FILL_BLANKS = "fill_blanks"
    MULTIPLE_CHOICE = "multiple_choice"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    preferred_language = Column(String, nullable=False)
    proficiency_level = Column(Integer, nullable=False)
    last_session_date = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    sessions = relationship("Session", back_populates="user")

class Session(Base):
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    format = Column(Enum(LearningFormat), nullable=False)
    topic = Column(String, nullable=True)  # For conversation and word gain
    grammar_format = Column(Enum(GrammarFormat), nullable=True)  # For grammar sessions
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    completion_status = Column(String, default="in_progress")
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    progress_entries = relationship("Progress", back_populates="session")

class Progress(Base):
    __tablename__ = "progress"
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    score = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    session = relationship("Session", back_populates="progress_entries")
