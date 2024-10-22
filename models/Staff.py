from Person import Person
from Order import Order

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class Staff(Person):
    def __init__(self, firstName: str, lastName: str, password: str, username: str, dateJoined: str, deptName: str, listOfCustomers: list, listOfOrders: list, premadeBoxes: list, staffID: int, veggies: list) -> None:
        """
        Initialize a Staff member with necessary details.
        :param firstName: First name of the staff member
        :param lastName: Last name of the staff member
        :param password: Password of the staff member
        :param username: Username of the staff member
        :param dateJoined: Date when the staff member joined
        :param deptName: Department name of the staff member
        :param listOfCustomers: List of customers associated with the staff member
        :param listOfOrders: List of orders processed by the staff member
        :param premadeBoxes: List of premade boxes handled by the staff member
        :param staffID: Unique staff ID
        :param veggies: List of veggies associated with the staff member
        """
        super().__init__(firstName, lastName, password, username)
        self.__dateJoined = dateJoined
        self.__deptName = deptName
        self.__listOfCustomers = listOfCustomers
        self.__listOfOrders = listOfOrders
        self.__premadeBoxes = premadeBoxes
        self.__staffID = staffID
        self.__veggies = veggies

    @property
    def dateJoined(self) -> str:
        """Return the date the staff member joined."""
        return self.__dateJoined

    @property
    def deptName(self) -> str:
        """Return the department name of the staff member."""
        return self.__deptName

    @property
    def listOfCustomers(self) -> list:
        """Return the list of customers associated with the staff member."""
        return self.__listOfCustomers

    @property
    def listOfOrders(self) -> list:
        """Return the list of orders processed by the staff member."""
        return self.__listOfOrders

    @property
    def premadeBoxes(self) -> list:
        """Return the list of premade boxes handled by the staff member."""
        return self.__premadeBoxes

    @property
    def staffID(self) -> int:
        """Return the staff ID."""
        return self.__staffID

    @property
    def veggies(self) -> list:
        """Return the list of veggies associated with the staff member."""
        return self.__veggies

    def get_details(self) -> str:
        return f"Staff: {self.firstName} {self.lastName}, ID: {self.__staffID}"

    def process_order(self, order: 'Order') -> None:
        """Process an order on behalf of the customer."""
        print(f"Processing order for {order.orderCustomer.get_details()}")
