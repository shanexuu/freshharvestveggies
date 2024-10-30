from sqlalchemy import Column, Integer, String,ForeignKey, Float, Date
from . import db

class Payment(db.Model):
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    paymentAmount = Column(Float)
    paymentDate = Column(Date)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    type = Column(String(50))


    __mapper_args__ = {
        'polymorphic_on': type,  
        'polymorphic_identity': 'payment' 
    }

    def __init__(self, paymentAmount, paymentDate,customer_id):
        self.paymentAmount = paymentAmount
        self.paymentDate = paymentDate
        self.customer_id = customer_id
        

    