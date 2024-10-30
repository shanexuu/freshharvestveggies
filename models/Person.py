from sqlalchemy import Column, Integer, String
from . import db
from .Item import Item
from .Veggie import Veggie
from .PremadeBox import PremadeBox
from flask import session
from .Order import Order
from .OrderLine import OrderLine



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
    

    def add_to_cart(self, item, quantity):

        """
        Adds an item to the cart. If the item already exists, increase its quantity.
        Args:
            item (Veggie or PremadeBox): The item to add.
            quantity (int): The quantity to add.
        """
        # Initialize cart from session if it exists, otherwise create a new one
        if 'cart' in session:
            self.cart = session['cart']
        else:
            self.cart = {}

        # Validate that quantity is positive
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        

        item_id = item.id  # Get the item's ID

        # Set the item name based on the type
        item_name = f"Premade Box - {item.boxSize}" if isinstance(item, PremadeBox) else item.vegName

        if item_id in self.cart:
            # Update quantity if item already in cart
            self.cart[item_id]["quantity"] += quantity
        else:
            # Add new item to cart
            self.cart[str(item_id)] = {
                "id": str(item_id),  # Include the item ID here
                "name": item_name,  
                "img": item.img_src,
                "price": item.get_price,
                "quantity": quantity,
            }

        # Update the session with the current cart
        session['cart'] = self.cart
    
       
        
        return f"{quantity} x {item_name} added to cart."
    
    def checkout(self, db_session):
        # Create a new order
        new_order = Order(orderCustomer=self.id)
        
        # Loop through items in the cart and create OrderLine entries
        for item_id, quantity in self.cart.items():
            # Create a new order line for each item in the cart
            order_line = OrderLine(order=new_order, item_id=item_id, quantity=quantity)
            new_order.listOfItems.append(order_line)
        
        # Add the order to the session and commit to save it in the database
        db_session.add(new_order)
        db_session.commit()
        
        # Clear the cart after checkout
        self.cart.clear()

        return new_order
    

    def checkout(self):
        raise NotImplementedError("Checkout method must be implemented in subclasses.")

            


        
        