from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from .Veggie import Veggie



class PackVeggie(Veggie):
    
    __tablename__ = 'packveggie'
    id = Column(Integer, ForeignKey('veggie.id'), primary_key=True)  
    pack=Column(Float)
    pricePerPack = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'packveggie',
    }

    def __init__(self, img_src, vegName, unit, pack, pricePerPack):
        super().__init__(img_src=img_src, vegName=vegName, unit=unit)
        self.vegType = 'packveggie'
        self.pack = pack
        self.pricePerPack = pricePerPack

    def __repr__(self):
        return f"<PackVeggie {self.id}: {self.vegName}, Price per pack: {self.pricePerPack}>"
