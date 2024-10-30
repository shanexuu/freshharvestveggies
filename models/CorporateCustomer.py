from sqlalchemy import Column, String, ForeignKey, Integer, Date, Float
from .Customer import db, Customer
from sqlalchemy.orm import relationship
from .Order import Order
from .OrderLine import OrderLine
from .AccountPayment import AccountPayment
from .CreditCardPayment import CreditCardPayment
from .DebitCardPayment import DebitCardPayment
from datetime import date

class CorporateCustomer(Customer):
    __tablename__ = 'corporatecustomer'
    id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    discountRate = Column(Float)
    maxCredit = Column(Float)
    minBalance = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'corporatecustomer', 
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance, maxOwing, discountRate, maxCredit, minBalance):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username,custAddress=custAddress, custBalance=custBalance, maxOwing=maxOwing)
        self.cusType = 'corporatecustomer'
        self.discountRate = discountRate
        self.maxCredit = maxCredit
        self.minBalance = minBalance
    

    # Method to display corporate customer profile
    def display_profile(self):
        """
        Returns the profile data for the corporate customer to be rendered.
        """
        profile_data = {
            'name': f"{self.firstName} {self.lastName}",
            'address': self.custAddress,
            'balance': self.custBalance,
            'maxOwing': self.maxOwing,
            'discountRate': self.discountRate,
            'maxCredit': self.maxCredit,
            'minBalance': self.minBalance,
          
        }
        return profile_data
    
    def checkout(self, cart, delivery_method, payment_method, payment_details):
        # Calculate total payment amount for the order
        payment_amount = sum(item['price'] * item['quantity'] for item in cart.values())

        # Apply corporate discount
        if isinstance(self, CorporateCustomer):  # Check if the customer is a corporate customer
            discount = payment_amount * (self.discountRate / 100)  # Calculate discount
            payment_amount -= discount  # Deduct discount from total amount

        # Add delivery fee if the selected delivery method is "Delivery"
        if delivery_method == "Delivery":
            payment_amount += 10.00 

        # Check if proceeding with the payment would exceed the customer's max owing
        if self.custBalance - payment_amount < -self.maxOwing:
            raise ValueError(f"Cannot place order: Outstanding balance exceeds allowed maximum of ${self.maxOwing}.")

        # Check if corporate customer's balance exceeds their credit limit
        if isinstance(self, CorporateCustomer) and self.custBalance + payment_amount > self.maxCredit:
            raise ValueError(f"Cannot place order: Outstanding balance exceeds allowed credit limit of ${self.maxCredit}.")

        # Create a new Order
        new_order = Order(
            customer_id=self.id,
            orderDate=date.today(),
            orderStatus="Processing",
            delivery=delivery_method,
        )

        # Add OrderLine items for each item in the cart
        for item in cart.values():
            # Access the item ID safely
            order_line = OrderLine(
                order=new_order,
                item_id=item['id'],  
                quantity=item['quantity']
            )
            new_order.listOfItems.append(order_line)

        # Create Payment based on selected payment method
        payment_date = date.today()
        
        if payment_method == "balance":
            if self.custBalance >= payment_amount:
                self.custBalance -= payment_amount
                payment = AccountPayment(paymentAmount=payment_amount, paymentDate=payment_date, customer_id=self.id)
            else:
                raise ValueError("Insufficient account balance for payment.")

        elif payment_method == "credit":
            payment = CreditCardPayment(
                paymentAmount=payment_amount,
                paymentDate=payment_date,
                customer_id=self.id,
                nameOncard=payment_details['nameOnCard'],
                cardNumber=payment_details['cardNumber'],
                expiration=payment_details['expiration'],
                cvv=payment_details['cvv']
            )

        elif payment_method == "debit":
            payment = DebitCardPayment(
                paymentAmount=payment_amount,
                paymentDate=payment_date,
                customer_id=self.id,
                nameOncard=payment_details['nameOnCard'],
                cardNumber=payment_details['cardNumber'],
                expiration=payment_details['expiration'],
                cvv=payment_details['cvv']
            )
        
        else:
            raise ValueError("Invalid payment method selected.")

        # Add order and payment to session and commit
        db.session.add(new_order)  # Add the new order to the session
        db.session.add(payment)     # Add the payment to the session
        db.session.commit()         # Commit the changes to the database

        # Return confirmation or order summary with the order ID
        return {"id": new_order.id, "total_amount": payment_amount, "payment_status": "Success"}


    
