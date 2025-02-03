import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from .models import Base

# Get database URL from environment or use default SQLite path
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/language_tutor.db')

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize the database, creating all tables"""
    Base.metadata.create_all(bind=engine)

@contextmanager
def get_db():
    """Get a database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_or_create_session_state(db, language: str, proficiency_level: int):
    """Get current session state or create new one"""
    from .models import SessionState, Conversation
    
    # Get latest session state
    session_state = db.query(SessionState).order_by(SessionState.created_at.desc()).first()
    
    if not session_state:
        # Create new conversation and session state
        conversation = Conversation(
            language=language,
            proficiency_level=proficiency_level
        )
        db.add(conversation)
        db.flush()
        
        session_state = SessionState(
            conversation_id=conversation.id,
            language=language,
            proficiency_level=proficiency_level
        )
        db.add(session_state)
        db.commit()
    
    return session_state
