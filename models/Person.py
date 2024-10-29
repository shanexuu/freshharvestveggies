
from sqlalchemy import Column, Integer, String

from . import db


class Person(db.Model):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    firstName = Column(String(255))
    lastName = Column(String(255))
    password = Column(String(255))
    username = Column(String(255))
    type = Column(String(50)) 

    __mapper_args__ = {
        'polymorphic_on': type,  
        'polymorphic_identity': 'person'  
    }

    def __init__(self,  firstName, lastName, password, username):
        self.firstName = firstName
        self.lastName = lastName
        self.password = password
        self.username= username

    def check_password(self, input_password):
        return self.password == input_password
    

    def add_to_cart(self, item, quantity=1):
        """
        Adds an item to the cart or updates the quantity if it already exists.
        Arguments:
            item (Item): The item object to be added to the cart.
            quantity (int): The quantity of the item to add. Defaults to 1.
        """
        item_id = item.id
        if item_id in self.cart:
            # Update quantity if item already in cart
            self.cart[item_id]["quantity"] += quantity
        else:
            # Add new item to cart
            self.cart[item_id] = {
                "name": item.name,
                "img": item.img_src,
                "price": item.get_price,
                "quantity": quantity
            }
        print(f"Added {quantity} of {item.name} to cart.")


    
    