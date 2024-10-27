from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Veggie import Veggie
from sqlalchemy.ext.hybrid import hybrid_property



class UnitPriceVeggie(Veggie):
    __tablename__ = 'unitpriceveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    vegUnit=Column(Integer)
  

    __mapper_args__ = {
        'polymorphic_identity': 'unitpriceveggie',
    }

    def __init__(self, img_src, vegName, unit, price,vegUnit):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit, price=price)
        self.vegType = 'unitpriceveggie'
        self.vegUnit= vegUnit
       

    

    def __repr__(self):
        return f"<UnitPriceVeggie {self.id}: {self.vegName}>"