from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, firstName: str, lastName: str, password: str, username: str) -> None:
        """
        Initialize a Person with a first name, last name, password, and username.
        :param firstName: First name of the person
        :param lastName: Last name of the person
        :param password: Password of the person
        :param username: Username of the person
        """
        self.__firstName = firstName
        self.__lastName = lastName
        self.__password = password
        self.__username = username

    @property
    def firstName(self) -> str:
        """Return the person's first name."""
        return self.__firstName

    @property
    def lastName(self) -> str:
        """Return the person's last name."""
        return self.__lastName

    @property
    def password(self) -> str:
        """Return the person's password."""
        return self.__password

    @property
    def username(self) -> str:
        """Return the person's username."""
        return self.__username

    @abstractmethod
    def get_details(self) -> str:
        """Abstract method to return person's details."""
        pass
