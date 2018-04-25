from sqlalchemy import Column, Integer, String
from db.models import Base


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    coordinates = Column(String)
    address = Column(String)
    building_name = Column(String)
    how_to_get_recommendation = Column(String)
    screen = Column(String)  # google maps photo ?


class Navigation(Base):
    __tablename__ = 'navigation'
    id = Column(Integer, primary_key=True)
