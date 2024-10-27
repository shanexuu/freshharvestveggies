from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property

from . import db

class Item(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    img_src = Column(String(255))
    type = Column(String(50)) 
    
    __mapper_args__ = {
        'polymorphic_on': type,  
        'polymorphic_identity': 'item' 
    }

   

    def __init__(self, img_src):
        self.img_src = img_src

    @hybrid_property
    def get_price(self):
     
        return 0

    def __repr__(self):
        return f"<Item {self.id}: {self.img_src}>"
