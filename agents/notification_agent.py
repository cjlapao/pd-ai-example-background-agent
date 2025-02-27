import logging
import asyncio
from typing import Dict, List, Any, Optional
from interfaces.background_agent import BackgroundAgent
from models.background_message import BackgroundMessage

logger = logging.getLogger(__name__)


class NotificationAgent(BackgroundAgent):
    """
    Example background agent that manages user notifications.

    This agent demonstrates:
    1. Message-driven processing (no timer)
    2. State management for multiple users
    3. Filtering and prioritizing notifications
    """

    def __init__(self, session_id: str):
        # Initialize without an interval (purely message-driven)
        super().__init__(
            session_id=session_id, agent_type="notification_manager", interval=None
        )

        # Subscribe to notification-related message types
        self.subscribe_to("notification.create")
        self.subscribe_to("notification.dismiss")
        self.subscribe_to("notification.list")
        self.subscribe_to("user.session.*")  # Track user sessions

        # Initialize notification storage
        self._notifications: Dict[str, List[Dict[str, Any]]] = {}
        self._user_sessions: Dict[str, bool] = {}

        logger.info(f"NotificationAgent initialized with session_id: {session_id}")

    async def process(self) -> None:
        """
        This agent doesn't use periodic processing, so this method is empty.
        All functionality is driven by messages.
        """
        pass

    async def process_message(self, message: BackgroundMessage) -> None:
        """
        Process incoming notification-related messages.
        """
        try:
            logger.info(f"Processing message: {message.message_type}")

            if message.message_type == "notification.create":
                await self._create_notification(message)

            elif message.message_type == "notification.dismiss":
                await self._dismiss_notification(message)

            elif message.message_type == "notification.list":
                await self._list_notifications(message)

            elif message.message_type == "user.session.start":
                await self._handle_session_start(message)

            elif message.message_type == "user.session.end":
                await self._handle_session_end(message)

        except Exception as e:
            logger.error(f"Error processing message {message.message_type}: {str(e)}")

    async def _create_notification(self, message: BackgroundMessage) -> None:
        """Create a new notification for a user"""
        if not message.data:
            logger.warning("Notification create message missing data")
            return

        user_id = message.data.get("user_id")
        if not user_id:
            logger.warning("Notification missing user_id")
            return

        notification = {
            "id": message.data.get(
                "id", f"notif_{len(self._notifications.get(user_id, []))}"
            ),
            "title": message.data.get("title", "Notification"),
            "message": message.data.get("message", ""),
            "type": message.data.get("type", "info"),
            "created_at": message.data.get(
                "created_at", asyncio.get_event_loop().time()
            ),
            "read": False,
            "dismissed": False,
        }

        # Initialize user's notification list if it doesn't exist
        if user_id not in self._notifications:
            self._notifications[user_id] = []

        # Add the notification
        self._notifications[user_id].append(notification)

        logger.info(f"Created notification for user {user_id}: {notification['title']}")

        # If user is active, we could send a real-time notification
        if self._user_sessions.get(user_id, False):
            logger.info(f"User {user_id} is active, sending real-time notification")
            # In a real implementation, you would send a WebSocket message or similar

    async def _dismiss_notification(self, message: BackgroundMessage) -> None:
        """Dismiss a notification for a user"""
        if not message.data:
            return

        user_id = message.data.get("user_id")
        notification_id = message.data.get("notification_id")

        if not user_id or not notification_id:
            logger.warning("Dismiss notification missing user_id or notification_id")
            return

        # Find and dismiss the notification
        if user_id in self._notifications:
            for notification in self._notifications[user_id]:
                if notification["id"] == notification_id:
                    notification["dismissed"] = True
                    logger.info(
                        f"Dismissed notification {notification_id} for user {user_id}"
                    )
                    break

    async def _list_notifications(self, message: BackgroundMessage) -> None:
        """List notifications for a user"""
        if not message.data:
            return

        user_id = message.data.get("user_id")
        include_dismissed = message.data.get("include_dismissed", False)

        if not user_id:
            logger.warning("List notifications missing user_id")
            return

        # Get notifications for the user
        user_notifications = self._notifications.get(user_id, [])

        # Filter out dismissed notifications if requested
        if not include_dismissed:
            user_notifications = [n for n in user_notifications if not n["dismissed"]]

        # Mark notifications as read
        for notification in user_notifications:
            notification["read"] = True

        logger.info(
            f"Listed {len(user_notifications)} notifications for user {user_id}"
        )

        # In a real implementation, you would send these notifications back to the requester

    async def _handle_session_start(self, message: BackgroundMessage) -> None:
        """Handle user session start"""
        if not message.data:
            return

        user_id = message.data.get("user_id")
        if not user_id:
            return

        # Mark user as active
        self._user_sessions[user_id] = True
        logger.info(f"User {user_id} session started")

        # Send any pending notifications
        pending_notifications = [
            n
            for n in self._notifications.get(user_id, [])
            if not n["read"] and not n["dismissed"]
        ]

        if pending_notifications:
            logger.info(
                f"User {user_id} has {len(pending_notifications)} pending notifications"
            )
            # In a real implementation, you would send these notifications to the user

    async def _handle_session_end(self, message: BackgroundMessage) -> None:
        """Handle user session end"""
        if not message.data:
            return

        user_id = message.data.get("user_id")
        if not user_id:
            return

        # Mark user as inactive
        self._user_sessions[user_id] = False
        logger.info(f"User {user_id} session ended")
