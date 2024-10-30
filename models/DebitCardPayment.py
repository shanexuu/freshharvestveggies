from .Payment import Payment

from sqlalchemy import Column, Integer, String,ForeignKey, Float, Date


class DebitCardPayment(Payment):

    __tablename__ = 'debitcardpayment'
    id = Column(Integer, ForeignKey('payment.id'), primary_key=True)
    nameOncard = Column(String(50))
    cardNumber = Column(String(255))
    expiration = Column(String(50))
    cvv = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity': 'debitcardpayment',
    }

    def __init__(self, paymentAmount, paymentDate,customer_id, nameOncard, cardNumber, expiration, cvv):
        super().__init__(paymentAmount=paymentAmount, paymentDate=paymentDate, customer_id=customer_id)
        self.type = 'debitcardpayment'
        self.nameOncard = nameOncard
        self.cardNumber = cardNumber
        self.expiration = expiration
        self.cvv = cvv