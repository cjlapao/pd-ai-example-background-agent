#!/usr/bin/env python3
"""
Example script demonstrating how to send messages to background agents.
This would typically be done from your application code.
"""

import asyncio
import json
import sys
import os

# Add the parent directory to the path so we can import the models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from models.background_message import BackgroundMessage


async def main():
    """Send example messages to background agents"""
    print("Sending example messages to background agents")

    # In a real application, you would use an API client or WebSocket to send these messages
    # For this example, we'll just print the messages that would be sent

    # Example 1: Request system status
    status_request = BackgroundMessage(message_type="system.status.request", data=None)
    print("\nExample 1: System Status Request")
    print(json.dumps(status_request.dict(), indent=2))

    # Example 2: Request specific resource information
    resource_request = BackgroundMessage(
        message_type="system.resource.request", data={"resource_type": "cpu"}
    )
    print("\nExample 2: Resource Request")
    print(json.dumps(resource_request.dict(), indent=2))

    # Example 3: Create a notification
    notification_create = BackgroundMessage(
        message_type="notification.create",
        data={
            "user_id": "user123",
            "title": "New Message",
            "message": "You have a new message from Alice",
            "type": "info",
        },
    )
    print("\nExample 3: Create Notification")
    print(json.dumps(notification_create.dict(), indent=2))

    # Example 4: User session start
    session_start = BackgroundMessage(
        message_type="user.session.start", data={"user_id": "user123"}
    )
    print("\nExample 4: User Session Start")
    print(json.dumps(session_start.dict(), indent=2))

    print("\nIn a real application, you would send these messages to the backend API:")
    print("POST /api/background/message")
    print("Content-Type: application/json")
    print("Authorization: Bearer YOUR_TOKEN")
    print("\n{message JSON}")


if __name__ == "__main__":
    asyncio.run(main())
