from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

class BaseModel:
    """Base model with common attributes"""
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Conversation(Base, BaseModel):
    """Represents a conversation session"""
    language = Column(String(50), nullable=False)
    proficiency_level = Column(Integer, nullable=False)
    current_topic = Column(String(200))
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base, BaseModel):
    """Individual messages in a conversation"""
    conversation_id = Column(Integer, ForeignKey('conversation.id'), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    corrections = Column(Text)  # JSON string of corrections
    conversation = relationship("Conversation", back_populates="messages")

class SessionState(Base, BaseModel):
    """Current session state and settings"""
    conversation_id = Column(Integer, ForeignKey('conversation.id'), nullable=False)
    language = Column(String(50), nullable=False)
    proficiency_level = Column(Integer, nullable=False)
    current_topic = Column(String(200))
    last_context = Column(Text)  # JSON string of last conversation context
    conversation = relationship("Conversation")
