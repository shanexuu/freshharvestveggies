from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Veggie import Veggie



class UnitPriceVeggie(Veggie):
    __tablename__ = 'unitpriceveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    vegUnit=Column(Integer)
    pricePerUnit = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'unitpriceveggie',
    }

    def __init__(self, img_src, vegName, unit, vegUnit, pricePerUnit):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit)
        self.vegType = 'unitpriceveggie'
        self.vegUnit= vegUnit
        self.pricePerUnit = pricePerUnit

    def __repr__(self):
        return f"<UnitPriceVeggie {self.id}: {self.vegName}, Price per unit: {self.pricePerUnit}>"