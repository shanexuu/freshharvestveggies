from sqlalchemy import Column, String, ForeignKey, Float, Integer
from .Item import Item
from . import db
from sqlalchemy.ext.hybrid import hybrid_property


class PremadeBox(Item):

    __tablename__ = 'premadebox'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    boxSize = Column(String(255))
    numOfBoxes = Column(Integer)
    boxContent = Column(String(255))
    price = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'premadebox',
    }

    def __init__(self, img_src,boxSize, numOfBoxes, boxContent,price):
        super().__init__(img_src=img_src)
        self.boxSize = boxSize
        self.numOfBoxes = numOfBoxes
        self.boxContent = boxContent
        self.price = price


    @hybrid_property
    def get_price(self):
        return self.price


    