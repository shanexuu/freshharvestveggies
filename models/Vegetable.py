from models.Item import Product
from sqlalchemy.ext.declarative import as_declarative, declared_attr


class Vegetable(Product):
    def __init__(self, name: str, price: float, unit: str, stock: int) -> None:
        """
        Initialize a Vegetable product.
        :param name: Name of the vegetable
        :param price: Price per unit
        :param unit: Unit of sale (e.g., bunch, kg)
        :param stock: Amount of stock available
        """
        super().__init__(name, price)
        self.__unit = unit
        self.__stock = stock

    @property
    def unit(self) -> str:
        """Return the unit of sale for the vegetable."""
        return self.__unit

    @property
    def stock(self) -> int:
        """Return the current stock of the vegetable."""
        return self.__stock

    def reduce_stock(self, quantity: int) -> None:
        """
        Reduce the stock level after a sale.
        :param quantity: Number of units sold
        :raises: if not enough stock
        """
        if quantity > self.__stock:
            raise ValueError("Not enough stock.")
        self.__stock -= quantity

    def get_price(self) -> float:
        """Return the price of the vegetable."""
        return self.price

    def get_details(self) -> str:
        """Return details about the vegetable."""
        return f"Vegetable: {self.name}, Unit: {self.__unit}, Price: {self.price}, Stock: {self.__stock}"
