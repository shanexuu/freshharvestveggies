from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Veggie import Veggie

class WeightedVeggie(Veggie):
    __tablename__ = 'weightedveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    weightUnit = Column(Float)
    pricePerWeight = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'weightedveggie', 
    }

    def __init__(self, img_src, vegName, unit, weightUnit, pricePerWeight):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit)
        self.vegType = 'weightedveggie'
        self.weightUnit = weightUnit
        self.pricePerWeight = pricePerWeight

    def __repr__(self):
        return f"<WeightedVeggie {self.id}: {self.vegName}, Price per kilo: {self.pricePerWeight}>"
