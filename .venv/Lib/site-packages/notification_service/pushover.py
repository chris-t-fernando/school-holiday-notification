# external packages
import logging
from pushover import Pushover as po

# my modules
from .inotification_service import INotificationService


log = logging.getLogger(__name__)


class Pushover(INotificationService):
    def __init__(
        self,
        api_key: str,
        user_key: str,
    ):
        self.client = po(api_key)
        self.client.user(user_key)

    def send(self, message: str, subject: str = None) -> bool:
        if not subject:
            subject = "tabot notification"

        po_message = self.client.msg(message)
        po_message.set("title", subject)
        self.client.send(po_message)


# finish changing get parameter and put parameter
# finish moving from two bools to just reading run_type
# generally just keep implementing new config objects
