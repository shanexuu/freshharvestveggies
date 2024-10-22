from Customer import Customer


class CorporateCustomer(Customer):
    def __init__(self, name: str, contact_info: str, balance: float, credit_limit: float) -> None:
        """
        Initialize a Corporate Customer.
        :param name: Name of the corporate customer
        :param contact_info: Contact information of the corporate customer
        :param balance: Corporate customer's account balance
        :param credit_limit: Credit limit for the corporate customer
        """
        super().__init__(name, contact_info, balance)
        self.__credit_limit = credit_limit

    @property
    def credit_limit(self) -> float:
        """Return the corporate customer's credit limit."""
        return self.__credit_limit
    
    def is_private(self) -> bool:
        return False

    def is_corporate(self) -> bool:
        return True
    

    def can_place_order(self, amount: float) -> bool:
        """Check if the corporate customer can place an order.
        Corporate customers cannot place an order if their balance is greater than their credit limit.
        return True if they can place an order, False otherwise
        """
        return self.balance <= self.__credit_limit

    def apply_discount(self, amount: float) -> float:
        """Corporate customers get a 10% discount on each order."""
        return amount * 0.9 

    def get_details(self) -> str:
        """Return details about the corporate customer."""
        return f"Corporate Customer: {self.name}, Balance: {self.balance}, Credit Limit: {self.__credit_limit}"
