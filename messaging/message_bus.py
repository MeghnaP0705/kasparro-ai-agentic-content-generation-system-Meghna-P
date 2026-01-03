from queue import Queue, Empty
from typing import Dict, List
from threading import Lock
from messaging.message_types import Message

class MessageBus:
    """Central message broker for agent communication."""

    def __init__(self):
        self._queues: Dict[str, Queue] = {}
        self._lock = Lock()

    def register_agent(self, agent_id: str):
        """Register an agent with the message bus."""
        with self._lock:
            if agent_id not in self._queues:
                self._queues[agent_id] = Queue()
                print(f"[MessageBus] Registered agent: {agent_id}")

    def send_message(self, message: Message):
        """Send message to target agent."""
        if message.receiver in self._queues:
            self._queues[message.receiver].put(message)
        else:
            print(f"[MessageBus] Warning: Agent {message.receiver} not registered")

    def receive_message(self, agent_id: str, timeout=1) -> Message:
        """Receive message for agent (blocking with timeout)."""
        if agent_id in self._queues:
            try:
                return self._queues[agent_id].get(timeout=timeout)
            except Empty:
                return None
        return None

    def broadcast(self, message: Message, exclude: List[str] = None):
        """Broadcast message to all agents except excluded."""
        exclude = exclude or []
        with self._lock:
            for agent_id in self._queues.keys():
                if agent_id not in exclude:
                    msg_copy = Message(
                        sender=message.sender,
                        receiver=agent_id,
                        message_type=message.message_type,
                        content=message.content,
                        timestamp=message.timestamp,
                        conversation_id=message.conversation_id,
                        reply_to=message.reply_to
                    )
                    self.send_message(msg_copy)
