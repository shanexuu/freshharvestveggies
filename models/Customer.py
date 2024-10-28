from sqlalchemy import Column, String, ForeignKey, Integer, Date, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from .Person import Person
from .Order import Order
from datetime import date
from sqlalchemy.orm.exc import NoResultFound
from . import db
from flask import Flask, render_template, request, url_for, redirect, session



class Customer(Person):

    __tablename__ = 'customer'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    custAddress = Column(String(255))
    custBalance = Column(Float)
    maxOwing = Column(Float)
    cusType = Column(String(50))

    orders = relationship("Order", back_populates="customer")

    __mapper_args__ = {
        'polymorphic_on': cusType, 
        'polymorphic_identity': 'customer',
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance, maxOwing):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username)
        self.custAddress = custAddress
        self.custBalance = custBalance
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
    
    def cancel_order(self, order_id):
        """
        Cancel an order for this customer by order_id.
        
        Args:
            order_id (int): The ID of the order to cancel.
            session (Session): SQLAlchemy session for database operations.
        
        Returns:
            str: Confirmation message for the canceled order or error message.
        """
        try:
            # Find the order by ID and ensure it belongs to this customer
            order = db.session.query(Order).filter_by(id=order_id, customer_id=self.id).one()

            # Check if the order is eligible to be canceled
            if order.orderStatus == "Processing":
                # Cancel the order
               order.orderStatus = "Canceled"
               db.session.add(order)

            #    if order.total_amount and self.custBalance is not None:
            #     self.custBalance += order.total_amount
            #     session.add(self)  # Update customer's balance in the database

               db.session.commit()
               return f"Order {order_id} has been successfully canceled."
            
            if order.orderStatus == "Fulfilled":
                return "Order has already been completed and cannot be canceled."
            elif order.orderStatus == "Canceled":
                return "Order has already been canceled."
    
            else:
                return None

        except NoResultFound:
            return f"Order {order_id} not found for this customer."
        except Exception as e:
            db.session.rollback()  
            return f"An error occurred while canceling the order: {e}"
    

       
        