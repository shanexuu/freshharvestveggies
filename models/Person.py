
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


    
    