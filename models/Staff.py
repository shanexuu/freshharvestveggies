from sqlalchemy import Column, String, ForeignKey, Integer, Date
from .Person import Person

from datetime import date
from sqlalchemy.orm import relationship


class Staff(Person):
    __tablename__ = 'staff'
    id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    dateJoined = Column(Date)
    deptName = Column(String(50))
    staffID = Column(Integer)
   
    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }

    def __init__(self, firstName, lastName, password, username,dateJoined, deptName, staffID):
        super().__init__(firstName=firstName, lastName=lastName, password=password, username=username)
        self.dateJoined = dateJoined
        self.deptName = deptName
        self.staffID = staffID
        self.listOfCustomers = []
        self.listOfOrders = []
        self.premadeBoxes =[]
        self.veggies = []
        self.type = 'staff'

        
    # Method to display staff profile
    def display_profile(self):
        """
        Returns the profile data for the staff to be rendered.
        """
        profile_data = {
            'name': f"{self.firstName} {self.lastName}",
            'dateJoined': self.dateJoined,
            'deptName': self.deptName,
            'staffID': self.staffID,
            
        }
        return profile_data

   