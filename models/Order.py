from typing import List, Tuple
from Customer import Customer
from models.Item import Product
from Vegetable import Vegetable
from AccountChargePayment import AccountChargePayment
from DebitCardPayment import DebitCardPayment
from CreditCardPayment import CreditCardPayment
from datetime import datetime
from Shipping import Shipping

class Order:
    def __init__(self, customer: Customer, shipping: Shipping, order_date: datetime = None) -> None:
        """
        Initialize an Order object.
        :param customer: The customer placing the order.
        :param shipping: The shipping details for the order.
        :param order_date: The date the order was placed. Defaults to current datetime if not provided.
        """
        self.__customer = customer  
        self.__items: List[Tuple[Product, int]] = []  
        self.__total_amount = 0.0 
        self.__shipping = shipping  
        self.__delivery_fee = shipping.delivery_fee  
        self.__order_date = order_date if order_date else datetime.now()  
    @property
    def customer(self) -> Customer:
        """Get the customer who placed the order."""
        return self.__customer

    @property
    def total_amount(self) -> float:
        """Get the total amount for the order (without delivery fee)."""
        return self.__total_amount

    @property
    def delivery_fee(self) -> float:
        """Get the delivery fee for the order."""
        return self.__delivery_fee
    
    @property
    def order_date(self) -> datetime:
        """Get the date the order was placed."""
        return self.__order_date

    def add_item(self, product: Product, quantity: int) -> None:
        """
        Add a product and its quantity to the order.
        :param product: The product being added.
        :param quantity: The quantity of the product.
        """
        self.__items.append((product, quantity))  
        self.__total_amount += product.get_price() * quantity  
        
        # If the product is a Vegetable, reduce its stock by the ordered quantity.
        if isinstance(product, Vegetable):
            product.reduce_stock(quantity)

    def checkout(self, payment_type: str) -> None:
        """
        Process the checkout and payment for the order.
        :param payment_type: The type of payment method ("account", "debit", or "credit").
        :raises ValueError: If the customer cannot place the order or if the payment fails.
        """
        # Calculate the total cost including delivery fee.
        total_with_delivery = self.__total_amount + self.__delivery_fee 
        # Apply customer-specific discount.
        total_with_discount = self.__customer.apply_discount(total_with_delivery)  

        # Check if the customer has enough balance or credit to place the order.
        if not self.__customer.can_place_order(total_with_discount):
            raise ValueError("Customer cannot place the order.")

        # Select the appropriate payment processor based on the payment type.
        if payment_type == "account":
            payment_processor = AccountChargePayment(self.__customer)
        elif payment_type == "debit":
            payment_processor = DebitCardPayment()
        elif payment_type == "credit":
            payment_processor = CreditCardPayment()
        else:
            raise ValueError(f"Unsupported payment type: {payment_type}")

        # Process the payment.
        if payment_processor.process_payment(total_with_discount):
            print("Payment successful!")
        else:
            raise ValueError("Payment failed!")

    def get_order_details(self) -> str:
        """
        Get the details of the order.
        :return: A string representation of the order details, including customer, items, and costs.
        """
        details = f"Order for: {self.__customer.get_details()}\nItems:\n"
        # List each item and its quantity in the order.
        for item, quantity in self.__items:
            details += f"- {item.get_details()} (Quantity: {quantity})\n"
      
        details += f"Total Amount: {self.__total_amount}, Delivery Fee: {self.__delivery_fee}, Order Date: {self.__order_date}"
        return details
