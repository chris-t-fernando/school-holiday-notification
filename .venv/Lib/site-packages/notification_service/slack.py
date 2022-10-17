# external packages
import logging
from slack_sdk import WebClient

# my modules
from .inotification_service import INotificationService


log = logging.getLogger(__name__)


class Slack(INotificationService):
    def __init__(self, bot_key: str, channel: str):
        self.channel = channel
        self.client = WebClient(token=bot_key)

    def send(self, message: str, subject: str = None) -> bool:
        self.client.chat_postMessage(
            channel=self.channel,
            text=message,
        )
