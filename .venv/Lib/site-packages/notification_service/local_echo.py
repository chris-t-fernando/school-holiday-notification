# external packages
import logging
from pushover import Pushover
from slack_sdk import WebClient

# my modules
from .inotification_service import INotificationService


log = logging.getLogger(
    __name__
)

class LocalEcho(INotificationService):
    def __init__(
        self,
        bot_key=None,
        channel=None
    ):
        ...

    def send(self, message: str, subject: str = None) -> bool:
        print(f"LocalEcho: {message}")