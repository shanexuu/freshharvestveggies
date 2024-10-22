from sqlalchemy import Column, String, ForeignKey, Integer
from .Item import db, Item

class Veggie(Item):
    __tablename__ = 'veggie'
    id = Column(Integer, ForeignKey('item.id'), primary_key=True)  # Ensure foreign key relationship
    vegName = Column(String(50), nullable=False)

    def __init__(self, img_src, vegName):
        super().__init__(img_src)
        self.vegName = vegName

    def __repr__(self):
        return f"<Veggie {self.id}: {self.vegName}, Image: {self.img_src}>"
