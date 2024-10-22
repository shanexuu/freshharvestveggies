from models.Item import Product

from typing import List

class PremadeBox(Product):
    def __init__(self, size: str, price: float, contents: List[str]) -> None:
        """
        Initialize a PremadeBox with a size, price, and list of contents.
        :param size: Size of the premade box (small, medium, large)
        :param price: Price of the box
        :param contents: List of items in the box
        """
        super().__init__("Premade Box", price)
        self.__size = size
        self.__contents = contents

    @property
    def size(self) -> str:
        """Return the size of the premade box."""
        return self.__size

    @property
    def contents(self) -> List[str]:
        """Return the contents of the premade box."""
        return self.__contents

    def get_price(self) -> float:
        """Return the price of the premade box."""
        return self.price

    def get_details(self) -> str:
        """Return details about the premade box."""
        return f"Premade Box: {self.__size}, Contents: {', '.join(self.__contents)}, Price: {self.price}"
