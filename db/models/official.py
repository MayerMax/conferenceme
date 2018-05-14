from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.models import Base


class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email_address = Column(String)
    password = Column(String)  # no hashes! no salt ! none at all
    description = Column(String)
    logo = Column(String)
    external_links = Column(String)
    tags = Column(String)
    headquarters = Column(String)

    def __repr__(self):
        return """
Welcome to the conference made by {},
We are: {},
if you have questions - email us: {},
Our contacts: {}
        """.format(self.name, self.description, self.email_address, self.external_links)


class Sponsor(Base):
    __tablename__ = 'sponsor'
    id = Column(Integer, primary_key=True)
    conf_id = Column(Integer, ForeignKey('conference.id'))
    name = Column(String)
    logo_path = Column(String)
    description = Column(String)
    external_links = Column(String)
    tags = Column(String)
    advertisement = Column(String)

    conference = relationship('Conference', backref='sponsors')
