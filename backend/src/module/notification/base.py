"""Base class for notification providers."""

from abc import ABC, abstractmethod

from module.models.bangumi import Notification
from module.network import RequestContent


class NotificationProvider(RequestContent, ABC):
    """Abstract base class for notification providers.

    All notification providers must inherit from this class and implement
    the send() and test() methods.
    """

    @abstractmethod
    async def send(self, notification: Notification) -> bool:
        """Send a notification.

        Args:
            notification: The notification data containing anime info.

        Returns:
            True if the notification was sent successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def test(self) -> tuple[bool, str]:
        """Test the notification provider configuration.

        Returns:
            A tuple of (success, message) where success is True if the test
            passed and message contains details about the result.
        """
        pass

    def _format_message(self, notify: Notification) -> str:
        """Format the default notification message.

        Args:
            notify: The notification data.

        Returns:
            Formatted message string.
        """
        import os
        import re
        # If official_title contains a full path like "D:\server\QB\Bangumi\", strip it
        title = notify.official_title
        if os.sep in title or (os.altsep and os.altsep in title):
            # Try to find the bangumi folder name (the folder before "Season X")
            # Strip drive letter and base paths
            normalized = os.path.normpath(title)
            parts = normalized.split(os.sep)
            # Find the part that looks like a bangumi title (not "Season X")
            bangumi_parts = []
            for part in parts:
                if re.match(r'^Season\s*\d+$', part, re.IGNORECASE):
                    break
                bangumi_parts.append(part)
            title = os.sep.join(bangumi_parts) if bangumi_parts else parts[-1]
        return (
            f"{title} 更新啦\n"
            f"更新集数： 第{notify.episode}集"
        )
