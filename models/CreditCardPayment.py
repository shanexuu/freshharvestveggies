from Payment import Payment

class CreditCardPayment(Payment):
    def __init__(self, amount: float, card_number: str, expiry_date: str, cvv: str) -> None:
        """
        Initialize a credit card payment.
        :param amount: Payment amount
        :param card_number: Credit card number
        :param expiry_date: Expiry date of the credit card
        :param cvv: CVV code of the credit card
        """
        super().__init__(amount)
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__cvv = cvv

    def process_payment(self) -> bool:
        """
        Process the credit card payment.
        For this example, we assume all payments are successful.
        :return: True if the payment is successful
        """
        print(f"Processing credit card payment of {self.amount}")
        return True
