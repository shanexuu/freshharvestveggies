from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Veggie import Veggie
from sqlalchemy.ext.hybrid import hybrid_property


class WeightedVeggie(Veggie):
    __tablename__ = 'weightedveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    weightUnit = Column(Float)
    

    __mapper_args__ = {
        'polymorphic_identity': 'weightedveggie', 
    }

    def __init__(self, img_src, price, vegName, unit, weightUnit):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit, price=price)
        self.vegType = 'weightedveggie'
        self.weightUnit = weightUnit
     

    
    def __repr__(self):
        return f"<WeightedVeggie {self.id}: {self.vegName}>"
