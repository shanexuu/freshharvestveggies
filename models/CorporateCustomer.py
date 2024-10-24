from sqlalchemy import Column, String, ForeignKey, Integer, Date, Float
from .Customer import db, Customer
from sqlalchemy.orm import relationship



class CorporateCustomer(Customer):
    __tablename__ = 'corporatecustomer'
    id = Column(Integer, ForeignKey('customer.id'), primary_key=True)
    discountRate = Column(Float)
    maxCredit = Column(Float)
    minBalance = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'corporatecustomer', 
    }

    def __init__(self, firstName, lastName, password, username,custAddress, custBalance, custID, maxOwing, discountRate, maxCredit, minBalance):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username,custAddress=custAddress, custBalance=custBalance, custID=custID, maxOwing=maxOwing)
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

   
