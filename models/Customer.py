from sqlalchemy import Column, String, ForeignKey, Integer, Date, Float
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