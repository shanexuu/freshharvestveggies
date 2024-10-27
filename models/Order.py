from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String,ForeignKey, Date, Float
from datetime import date
from .Veggie import Veggie
from .Item import Item
from .PremadeBox import PremadeBox
from .WeightedVeggie import WeightedVeggie
from .PackVeggie import PackVeggie
from .UnitPriceVeggie import UnitPriceVeggie
from .OrderLine import OrderLine
from . import db
from flask import Flask, render_template, request, url_for, redirect, session

from sqlalchemy.orm import sessionmaker
class Order(db.Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    orderDate = Column(Date)
    orderStatus = Column(String(50))

    customer = relationship("Customer", back_populates="orders")
    listOfItems = relationship("OrderLine", back_populates="order")

    def __init__(self, orderCustomer, orderDate=date.today(), orderStatus="Processing"):
        self.orderCustomer = orderCustomer
        self.orderDate = orderDate
        self.orderStatus = orderStatus

    #Method to display order details for a customer
    @classmethod
    def display_orders(cls, customer):
      """
      Returns a list of dictionaries containing all orders and items for a given customer, with order total prices.
      """
      if not customer.orders:
        return []
    
      order_details_list = []
    
      for order in customer.orders:
    
        order_details = {
            "id": order.id,
            "orderDate": order.orderDate,
            "orderStatus": order.orderStatus,
            "listOfItems": [],

        }

        for order_line in order.listOfItems:
            item = order_line.item  # Retrieve the item from the order line
            quantity = order_line.quantity
            item_details = {
                "item_id": item.id,
                "img": "",
                "quantity": quantity,
                "name": "",    
            }  
            # Set the item name
            item_details["name"] = item.vegName if isinstance(item, Veggie) else item.boxContent
            
        
        order_details_list.append(order_details)
    
      return order_details_list


    def get_order_details(order_id):
        """
        Retrieve the details of a specific order by its ID.
        """
        order = db.session.query(Order).get(order_id)

        if not order:
            return None

        order_details = {
            "id": order.id,
            "orderDate": order.orderDate,
            "orderStatus": order.orderStatus,
            "listOfItems": [],
            "total_price": 0
        }

        for order_line in order.listOfItems:
           
            item = order_line.item  # Retrieve the item from the order line
            quantity = order_line.quantity
            item_price = item.get_price
            item_details = {
                "item_id": item.id,
                "quantity": quantity,
                "name": "", 
                "img": item.img_src,
                "price": item_price,  
                "total_item_price": item_price * quantity
              
            }  
            
            if isinstance(item, Veggie):
                item_details["name"] = item.vegName
            elif isinstance(item, PremadeBox):
                item_details["name"] = item.boxContent

          
            
            # Append item details to the list
            order_details["listOfItems"].append(item_details)
        
             # Add to total price of the order
            order_details["total_price"] += item_details["total_item_price"]


        return order_details   
    



    # def customer(self) -> Customer:
    #     """Get the customer who placed the order."""
    #     return self.__customer

    # @property
    # def total_amount(self) -> float:
    #     """Get the total amount for the order (without delivery fee)."""
    #     return self.__total_amount

    # @property
    # def delivery_fee(self) -> float:
    #     """Get the delivery fee for the order."""
    #     return self.__delivery_fee
    
    # @property
    # def order_date(self) -> datetime:
    #     """Get the date the order was placed."""
    #     return self.__order_date

    # def add_item(self, product: Product, quantity: int) -> None:
    #     """
    #     Add a product and its quantity to the order.
    #     :param product: The product being added.
    #     :param quantity: The quantity of the product.
    #     """
    #     self.__items.append((product, quantity))  
    #     self.__total_amount += product.get_price() * quantity  
        
    #     # If the product is a Vegetable, reduce its stock by the ordered quantity.
    #     if isinstance(product, Vegetable):
    #         product.reduce_stock(quantity)

    # def checkout(self, payment_type: str) -> None:
    #     """
    #     Process the checkout and payment for the order.
    #     :param payment_type: The type of payment method ("account", "debit", or "credit").
    #     :raises ValueError: If the customer cannot place the order or if the payment fails.
    #     """
    #     # Calculate the total cost including delivery fee.
    #     total_with_delivery = self.__total_amount + self.__delivery_fee 
    #     # Apply customer-specific discount.
    #     total_with_discount = self.__customer.apply_discount(total_with_delivery)  

    #     # Check if the customer has enough balance or credit to place the order.
    #     if not self.__customer.can_place_order(total_with_discount):
    #         raise ValueError("Customer cannot place the order.")

    #     # Select the appropriate payment processor based on the payment type.
    #     if payment_type == "account":
    #         payment_processor = AccountChargePayment(self.__customer)
    #     elif payment_type == "debit":
    #         payment_processor = DebitCardPayment()
    #     elif payment_type == "credit":
    #         payment_processor = CreditCardPayment()
    #     else:
    #         raise ValueError(f"Unsupported payment type: {payment_type}")

    #     # Process the payment.
    #     if payment_processor.process_payment(total_with_discount):
    #         print("Payment successful!")
    #     else:
    #         raise ValueError("Payment failed!")

    # def get_order_details(self) -> str:
    #     """
    #     Get the details of the order.
    #     :return: A string representation of the order details, including customer, items, and costs.
    #     """
    #     details = f"Order for: {self.__customer.get_details()}\nItems:\n"
    #     # List each item and its quantity in the order.
    #     for item, quantity in self.__items:
    #         details += f"- {item.get_details()} (Quantity: {quantity})\n"
      
    #     details += f"Total Amount: {self.__total_amount}, Delivery Fee: {self.__delivery_fee}, Order Date: {self.__order_date}"
    #     return details
