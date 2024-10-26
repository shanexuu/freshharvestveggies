from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String,ForeignKey, Date, Float


from . import db


class OrderLine(db.Model):
    __tablename__ = 'orderline'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.id'))
    item_id = Column(Integer, ForeignKey('item.id'))
    
    quantity = Column(Integer, nullable=False) 
    order = relationship("Order", back_populates="listOfItems")
    item = relationship("Item")