import sys

import settings

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    description = Column(Text())
    items = relationship("Item", back_populates="category")

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id,
            'items' : [x.serialize for x in self.items]
        }

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key = True)
    name = Column(String(200), nullable = False)
    description = Column(Text())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, back_populates="items")

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.id,
        }

# If this script is called, 
# it will create de database and table structures
if __name__ == '__main__':
    engine = create_engine(settings.DATABASE)
    Base.metadata.create_all(engine)