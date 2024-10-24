from sqlalchemy import Column, String, ForeignKey, Integer
from .Item import Item
from . import db

class Veggie(Item):
    __tablename__ = 'veggie'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)  
    vegName = Column(String(50), nullable=False)
    vegType = Column(String(50))
    unit = Column(String(50))

    __mapper_args__ = {
        'polymorphic_on': vegType, 
        'polymorphic_identity': 'veggie',
    }

    def __init__(self, img_src, vegName, unit):
        super().__init__(img_src=img_src)
        self.vegName = vegName
        self.unit = unit
        self.type = 'veggie'

    def __repr__(self):
        return f"<Veggie {self.id}: {self.vegName}, Image: {self.img_src}>"