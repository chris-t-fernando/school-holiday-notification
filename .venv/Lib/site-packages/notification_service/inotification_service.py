from abc import ABC, abstractmethod


class INotificationService(ABC):
    @abstractmethod
    def __init__(
        self,
        back_testing: bool,
        real_money_trading: bool = False,
    ):
        ...

    @abstractmethod
    def send(self, message: str, subject: str = None) -> bool:
        ...
