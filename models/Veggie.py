from sqlalchemy import Column, String,Float, ForeignKey, Integer
from .Item import Item
from . import db
from sqlalchemy.ext.hybrid import hybrid_property


class Veggie(Item):
    __tablename__ = 'veggie'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)  
    vegName = Column(String(50), nullable=False)
    vegType = Column(String(50))
    unit = Column(String(50))
    price = Column(Float)

    __mapper_args__ = {
        'polymorphic_on': vegType, 
        'polymorphic_identity': 'veggie',
    }

    def __init__(self, img_src, vegName, unit,price):
        super().__init__(img_src=img_src)
        self.vegName = vegName
        self.unit = unit
        self.price = price
        self.type = 'veggie'

    @hybrid_property
    def get_price(self):
        return self.price

    def __repr__(self):
        return f"<Veggie {self.id}: {self.vegName}, Image: {self.img_src}>"