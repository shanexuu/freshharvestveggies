from Customer import Customer


class PrivateCustomer(Customer):
    def __init__(self, name: str, contact_info: str, balance: float) -> None:
        """
        Initialize a Private Customer.
        :param name: Name of the private customer
        :param contact_info: Contact information of the private customer
        :param balance: Private customer's account balance
        """
        super().__init__(name, contact_info, balance)

    def is_private(self) -> bool:
        return True

    def is_corporate(self) -> bool:
        return False

    def can_place_order(self, amount: float) -> bool:
        """Check if the private customer can place an order.
        Private customers cannot place an order if the amount owing is greater than $100.00. 
        return True if they can place an order, False otherwise"""
        return self.balance <= 100

    def apply_discount(self, amount: float) -> float:
        """Private customers do not receive a discount, return the original amount."""
        return amount  

    def get_details(self) -> str:
        """Return details about the private customer."""
        return f"Private Customer: {self.name}, Balance: {self.balance}"
