from abc import ABC, abstractmethod

class Payment(ABC):
    def __init__(self, amount: float) -> None:
        """
        Initialize a payment with a specified amount.
        :param amount: Amount of the payment
        """
        self.__amount = amount

    @property
    def amount(self) -> float:
        """Return the payment amount."""
        return self.__amount

    @abstractmethod
    def process_payment(self) -> bool:
        """Abstract method to process the payment."""
        pass
