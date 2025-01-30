import json
from datetime import datetime
from sqlalchemy.orm import Session
from .models import Conversation, Message, SessionState

class ConversationRepository:
    """Repository for handling conversation-related database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_message(self, conversation_id: int, role: str, content: str, corrections: dict = None) -> Message:
        """Create a new message in the conversation"""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            corrections=json.dumps(corrections) if corrections else None
        )
        self.db.add(message)
        self.db.commit()
        return message
    
    def _message_to_dict(self, message: Message) -> dict:
        """Convert a Message object to a dictionary"""
        return {
            "id": message.id,
            "role": message.role,
            "content": message.content,
            "corrections": message.corrections,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat() if message.updated_at else None
        }
    
    def get_conversation_history(self, conversation_id: int, limit: int = 10) -> list[dict]:
        """Get recent messages from a conversation"""
        messages = (self.db.query(Message)
                   .filter(Message.conversation_id == conversation_id)
                   .order_by(Message.created_at.desc())
                   .limit(limit)
                   .all())
        return [self._message_to_dict(msg) for msg in messages]
    
    def update_session_state(self, session_id: int, **kwargs) -> SessionState:
        """Update session state with new values"""
        session_state = self.db.query(SessionState).get(session_id)
        for key, value in kwargs.items():
            if hasattr(session_state, key):
                setattr(session_state, key, value)
        
        session_state.updated_at = datetime.utcnow()
        self.db.commit()
        return session_state
    
    def get_current_session(self) -> SessionState:
        """Get the most recent session state"""
        return (self.db.query(SessionState)
                .order_by(SessionState.created_at.desc())
                .first())
