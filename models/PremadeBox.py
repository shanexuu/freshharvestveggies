from sqlalchemy import Column, String, ForeignKey, Integer
from .Item import Item
from . import db

class PremadeBox(Item):

    __tablename__ = 'premadebox'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)
    boxSize = Column(String(255))
    numOfBoxes = Column(Integer)
    boxContent = Column(String(255))

    __mapper_args__ = {
        'polymorphic_identity': 'premadebox',
    }

    def __init__(self, img_src, boxSize, numOfBoxes, boxContent):
        super().__init__(img_src=img_src)
        self.boxSize = boxSize
        self.numOfBoxes = numOfBoxes
        self.boxContent = boxContent


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
