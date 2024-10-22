from Payment import Payment
from Customer import Customer
from PrivateCustomer import PrivateCustomer
from CorporateCustomer import CorporateCustomer

class AccountChargePayment(Payment):
    def __init__(self, amount: float, customer: Customer) -> None:
        """
        Initialize an account charge payment.
        :param amount: Payment amount
        :param customer: The customer who is charged
        """
        super().__init__(amount)
        self.__customer = customer

    def process_payment(self) -> bool:
        """
        Process the account charge payment.
        :return: True if the customer has enough balance or credit to charge
        """
        if isinstance(self.__customer, PrivateCustomer) and self.__customer.balance > 100:
            print("Private customer cannot charge more than $100.")
            return False
        elif isinstance(self.__customer, CorporateCustomer) and self.__customer.balance < self.__customer.credit_limit:
            print("Corporate customer balance is below the credit limit.")
            return False
        else:
            self.__customer.balance -= self.amount
            print(f"Charging {self.amount} to the account of {self.__customer.name}")
            return True
