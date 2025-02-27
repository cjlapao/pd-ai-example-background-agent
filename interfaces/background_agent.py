from abc import ABC, abstractmethod
from typing import Optional, Set
from models.background_message import BackgroundMessage


class BackgroundAgent(ABC):
    """
    Abstract base class for background agents.

    This is a simplified version for demonstration purposes.
    In the actual application, this would be imported from the core library.
    """

    def __init__(
        self, session_id: str, agent_type: str, interval: Optional[float] = None
    ):
        """
        Initialize a background agent.

        Args:
            session_id: The session ID this agent is associated with
            agent_type: Unique identifier for this type of agent
            interval: Optional interval in seconds for periodic processing
        """
        self.session_id = session_id
        self._agent_type = agent_type
        self.interval = interval
        self.subscribed_messages: Set[str] = set()
        self._is_running = False

    @abstractmethod
    async def process(self) -> None:
        """
        Process timer-based work.

        This method is called periodically based on the interval.
        If interval is None, this method is never called automatically.
        """
        pass

    @abstractmethod
    async def process_message(self, message: BackgroundMessage) -> None:
        """
        Process message-based work.

        This method is called when a message matching one of the subscribed
        message types is received.

        Args:
            message: The message to process
        """
        pass

    def subscribe_to(self, message_type: str) -> None:
        """
        Subscribe to a message type.

        Message types can include wildcards, e.g., "user.action.*"

        Args:
            message_type: The message type to subscribe to
        """
        self.subscribed_messages.add(message_type)

    @property
    def agent_type(self) -> str:
        """Unique identifier for this type of agent"""
        return self._agent_type
