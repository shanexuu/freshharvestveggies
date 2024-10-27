from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Veggie import Veggie
from sqlalchemy.ext.hybrid import hybrid_property




class PackVeggie(Veggie):
    
    __tablename__ = 'packveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    pack=Column(Integer)
    

    __mapper_args__ = {
        'polymorphic_identity': 'packveggie',
    }

    def __init__(self, img_src, vegName, unit, price, pack):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit, price=price)
        self.vegType = 'packveggie'
        self.pack = pack
      

    

    def __repr__(self):
        return f"<PackVeggie {self.id}: {self.vegName}>"
