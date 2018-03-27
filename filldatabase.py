
import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Category, Base, Item

engine = create_engine(settings.DATABASE)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def add_category(session, name, description):
    c1 = Category()
    c1.name = name
    c1.description = description
    session.add(c1)
    return c1

def add_item(session, category, name, description):
    i = Item()
    i.name = name
    i.description = description
    i.category = category
    session.add(i)
    return i

if __name__ == '__main__':
    c1 = add_category(session, 'FPS', 'First Person Shooter')
    c2 = add_category(session, 'RPG', 'Role Playing Game')
    c3 = add_category(session, 'Side Scrolling', 'Side Scrolling')
    c4 = add_category(session, 'Point and Click', 'Point and Ckick')
    c5 = add_category(session, 'Survival Horror', 'Survival Horror')
    session.commit()

    i1 = add_item(session, c1, 'Doom', 'The father of FPS games.')
    i2 = add_item(session, c1, 'Wolfstein', 'The grandfather of FPS games.')
    i3 = add_item(session, c2, 'Skyrim', 'The Elder Scrolls - Skyrim.')
    i4 = add_item(session, c2, 'Diablo 3', '')
    i5 = add_item(session, c2, 'Legend Of Zelda', '')
    i6 = add_item(session, c3, 'Super Mario World', '')
    i7 = add_item(session, c5, 'Resident Evil', '')
    i8 = add_item(session, c4, 'Myst', '')
    session.commit()





