from Payment import Payment

class DebitCardPayment(Payment):
    def __init__(self, amount: float, card_number: str, expiry_date: str, cvv: str) -> None:
        """
        Initialize a debit card payment.
        :param amount: Payment amount
        :param card_number: Debit card number
        :param expiry_date: Expiry date of the debit card
        :param cvv: CVV code of the debit card
        """
        super().__init__(amount)
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__cvv = cvv

    def process_payment(self) -> bool:
        """
        Process the debit card payment.
        For this example, we assume all payments are successful.
        :return: True if the payment is successful
        """
        print(f"Processing debit card payment of {self.amount}")
        return True
