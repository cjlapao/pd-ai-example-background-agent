from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
import time


class BackgroundMessage(BaseModel):
    """
    Model representing a message sent to background agents.

    This is a simplified version for demonstration purposes.
    In the actual application, this would be imported from the core library.
    """

    message_type: str = Field(
        ..., description="Type of message, used for routing to appropriate agents"
    )
    data: Optional[Dict[str, Any]] = Field(None, description="Message payload data")
    timestamp: float = Field(
        default_factory=time.time,
        description="Unix timestamp when the message was created",
    )
    sender: str = Field(default="system", description="Identifier of the sender")

    def dict(self, *args, **kwargs):
        """Convert to dictionary, ensuring all values are JSON serializable"""
        result = super().dict(*args, **kwargs)
        return result
