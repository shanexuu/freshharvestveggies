from .Payment import Payment
from sqlalchemy import Column, Integer, String,ForeignKey, Float, Date


class AccountPayment(Payment):
    __tablename__ = 'accountpayment'
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'accountpayment',
    }

    def __init__(self, paymentAmount, paymentDate,customer_id):
        super().__init__(paymentAmount=paymentAmount, paymentDate=paymentDate, customer_id=customer_id)
        self.type = 'accountpayment'