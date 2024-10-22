from abc import ABC, abstractmethod
from typing import List
from Person import Person
from Order import Order

class Customer(Person, ABC):
    def __init__(self, firstName: str, lastName: str, password: str, username: str, custAddress: str, custBalance: float, custID: int, maxOwing: float) -> None:
        """
        Initialize a Customer with necessary details.
        :param firstName: First name of the customer
        :param lastName: Last name of the customer
        :param password: Password of the customer
        :param username: Username of the customer
        :param custAddress: Address of the customer
        :param custBalance: Customer's account balance
        :param custID: Customer ID
        :param maxOwing: Maximum amount the customer can owe
        """
        super().__init__(firstName, lastName, password, username)
        self.__custAddress = custAddress
        self.__custBalance = custBalance
        self.__custID = custID
        self.__maxOwing = maxOwing
        self.__order_history: List[Order] = []

    @property
    def custAddress(self) -> str:
        """Return the customer's address."""
        return self.__custAddress

    @property
    def custBalance(self) -> float:
        """Return the customer's balance."""
        return self.__custBalance

    @custBalance.setter
    def custBalance(self, amount: float) -> None:
        self.__custBalance = amount

    @property
    def custID(self) -> int:
        """Return the customer's ID."""
        return self.__custID

    @property
    def maxOwing(self) -> float:
        """Return the maximum owing amount."""
        return self.__maxOwing

    @property
    def order_history(self) -> List['Order']:
        """Return the customer's order history."""
        return self.__order_history

    @abstractmethod
    def is_private(self) -> bool:
        pass

    @abstractmethod
    def is_corporate(self) -> bool:
        pass

    @abstractmethod
    def can_place_order(self, amount: float) -> bool:
        """Abstract method to check if customer can place an order based on balance or credit."""
        pass

    @abstractmethod
    def apply_discount(self, amount: float) -> float:
        """Abstract method to apply a discount for the customer."""
        pass
