from dataclasses import dataclass
from typing import Any, Optional
from datetime import datetime
from enum import Enum

class MessageType(Enum):
    """Types of messages agents can exchange."""
    REQUEST = "request"
    RESPONSE = "response"
    INFORM = "inform"
    QUERY = "query"
    COMPLETE = "complete"
    ERROR = "error"

@dataclass
class Message:
    """Message structure for agent communication."""
    sender: str
    receiver: str
    message_type: MessageType
    content: Any
    timestamp: datetime
    conversation_id: str
    reply_to: Optional[str] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
