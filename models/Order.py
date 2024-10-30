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
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    orderDate = Column(Date)
    orderStatus = Column(String(50))
    delivery = Column(String(255))
    customer = relationship("Customer", back_populates="orders")
    listOfItems = relationship("OrderLine", back_populates="order")


    def __init__(self, customer_id, orderDate, orderStatus, delivery):
        self.customer_id = customer_id
        self.orderDate = orderDate
        self.orderStatus = orderStatus
        self.delivery = delivery

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
           
            item = order_line.item 
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
