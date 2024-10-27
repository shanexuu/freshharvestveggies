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


    # @property
    # def size(self) -> str:
    #     """Return the size of the premade box."""
    #     return self.__size

    # @property
    # def contents(self) -> List[str]:
    #     """Return the contents of the premade box."""
    #     return self.__contents

    # def get_price(self) -> float:
    #     """Return the price of the premade box."""
    #     return self.price

    # def get_details(self) -> str:
    #     """Return details about the premade box."""
    #     return f"Premade Box: {self.__size}, Contents: {', '.join(self.__contents)}, Price: {self.price}"
