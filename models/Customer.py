from sqlalchemy import Column, String, ForeignKey, Integer, Date, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from .Person import db, Person
from datetime import date


class Customer(Person):

    __tablename__ = 'customer'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    custAddress = Column(String(255))
    custBalance = Column(Float)
    custID = Column(Integer)
    maxOwing = Column(Float)
    cusType = Column(String(50))

    orders = relationship("Order", back_populates="customer")

    __mapper_args__ = {
        'polymorphic_on': cusType, 
        'polymorphic_identity': 'customer',
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance, custID, maxOwing):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username)
        self.custAddress = custAddress
        self.custBalance = custBalance
        self.custID = custID
        self.maxOwing = maxOwing
        self.type = 'customer'

   # Method to display customer profile
    def display_profile(self):
        """
        Returns the profile data for the customer to be rendered.
        """
        profile_data = {
            'name': f"{self.firstName} {self.lastName}",
            'address': self.custAddress,
            'balance': self.custBalance,
            'maxOwing': self.maxOwing,
          
        }
        return profile_data
    
    # Method to display customer orders
    def display_orders(self):
        """
        Returns the order details for the customer to be rendered.
        """
        if not self.orders:
            return "No orders found for this customer."

        order_details_list = []
        for order in self.orders:
            order_details = f"Order ID: {order.id}\n"
            order_details += f"Order Date: {order.orderDate}\n"
            order_details += f"Order Status: {order.orderStatus}\n"
            order_details += "Items:\n"
            
            for order_line in order.listOfItems:
                order_details += f"  - Item ID: {order_line.item_id}, Quantity: {order_line.quantity}\n"
            
            order_details_list.append(order_details)

        return "\n".join(order_details_list)