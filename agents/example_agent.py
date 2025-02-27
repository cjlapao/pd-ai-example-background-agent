import logging
import asyncio
import time
from typing import Dict, Any, Optional
from interfaces.background_agent import BackgroundAgent
from models.background_message import BackgroundMessage

logger = logging.getLogger(__name__)


class SystemMonitorAgent(BackgroundAgent):
    """
    Example background agent that monitors system resources and responds to status requests.

    This agent demonstrates:
    1. Periodic processing with an interval
    2. Message subscription and handling
    3. Basic state management
    """

    def __init__(self, session_id: str):
        # Initialize with a 60-second interval for periodic processing
        super().__init__(
            session_id=session_id, agent_type="system_monitor", interval=60.0
        )

        # Subscribe to message types this agent should handle
        self.subscribe_to("system.status.request")
        self.subscribe_to("system.resource.request")
        self.subscribe_to("user.action.*")  # Wildcard subscription for all user actions

        # Initialize agent state
        self._last_check_time = time.time()
        self._system_stats = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "uptime": 0,
            "active_users": 0,
        }

        logger.info(f"SystemMonitorAgent initialized with session_id: {session_id}")

    async def process(self) -> None:
        """
        Periodic processing method called based on the interval.
        This is where you put code that should run regularly.
        """
        try:
            # Record the current time
            current_time = time.time()
            elapsed = current_time - self._last_check_time
            self._last_check_time = current_time

            # Update system statistics (in a real agent, you would get actual system metrics)
            self._system_stats["uptime"] += elapsed

            # Simulate CPU and memory usage changes
            import random

            self._system_stats["cpu_usage"] = random.uniform(5.0, 95.0)
            self._system_stats["memory_usage"] = random.uniform(20.0, 80.0)

            logger.info(f"SystemMonitorAgent processed: {self._system_stats}")

            # In a real agent, you might:
            # 1. Check if any metrics exceed thresholds
            # 2. Send notifications if issues are detected
            # 3. Log historical data for trends
            # 4. Update a dashboard or status page

        except Exception as e:
            logger.error(f"Error in SystemMonitorAgent.process: {str(e)}")

    async def process_message(self, message: BackgroundMessage) -> None:
        """
        Process incoming messages that this agent has subscribed to.
        """
        try:
            logger.info(f"Processing message: {message.message_type}")

            # Handle different message types
            if message.message_type == "system.status.request":
                await self._handle_status_request(message)

            elif message.message_type == "system.resource.request":
                await self._handle_resource_request(message)

            elif message.message_type.startswith("user.action."):
                await self._handle_user_action(message)

        except Exception as e:
            logger.error(f"Error processing message {message.message_type}: {str(e)}")

    async def _handle_status_request(self, message: BackgroundMessage) -> None:
        """Handle requests for system status"""
        # In a real agent, you would send a response back to the requester
        logger.info(f"Status request received from {message.sender}")
        logger.info(f"Current system status: {self._system_stats}")

        # Example of how you might respond (in a real implementation)
        # await self._send_response(message.sender, {
        #     "status": "healthy" if self._system_stats["cpu_usage"] < 80.0 else "degraded",
        #     "metrics": self._system_stats
        # })

    async def _handle_resource_request(self, message: BackgroundMessage) -> None:
        """Handle requests for specific resource information"""
        resource_type = message.data.get("resource_type") if message.data else None

        if resource_type == "cpu":
            logger.info(f"CPU usage: {self._system_stats['cpu_usage']}%")
        elif resource_type == "memory":
            logger.info(f"Memory usage: {self._system_stats['memory_usage']}%")
        elif resource_type == "uptime":
            uptime_hours = self._system_stats["uptime"] / 3600
            logger.info(f"System uptime: {uptime_hours:.2f} hours")
        else:
            logger.info(f"Unknown resource type requested: {resource_type}")

    async def _handle_user_action(self, message: BackgroundMessage) -> None:
        """Handle user action messages"""
        action_type = message.message_type.replace("user.action.", "")

        # Track user activity (in a real agent, you might store this in a database)
        logger.info(f"User action detected: {action_type}")

        # Update active users count for demonstration
        if action_type == "login":
            self._system_stats["active_users"] += 1
        elif action_type == "logout":
            self._system_stats["active_users"] = max(
                0, self._system_stats["active_users"] - 1
            )
