from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String

db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    img_src = Column(String(255), nullable=False)

    def __init__(self, img_src):
        self.img_src = img_src

    def __repr__(self):
        return f"<Item {self.id}: {self.img_src}>"
