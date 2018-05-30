from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.models import Base


class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    conf_id = Column(Integer, ForeignKey('conference.id'))
    name = Column(String)
    tags = Column(String)
    external_links = Column(String)
    description = Column(String)
    logo_path = Column(String)
    conference = relationship('Conference', backref='sections')


class Lecture(Base):
    __tablename__ = 'lecture'
    id = Column(Integer, primary_key=True)
    section_id = Column(Integer, ForeignKey('section.id'))
    conf_id = Column(Integer, ForeignKey('conference.id'))
    topic = Column(String)
    description = Column(String)
    room = Column(String)
    tags = Column(String)
    keywords = Column(String)
    when = Column(DateTime)
    duration = Column(String)  # ?

    section = relationship('Section', backref='lectures')

    def __repr__(self):
        return """
title: {},
keywords: {},
at {}, in {}.
Length:{}

        """.format(self.topic, self.keywords, self.when.strftime("%Y-%m-%d-%H.%M"), self.room, self.duration)

    def get_description(self):
        return """
title: {},
 about: {},
        
keywords: {},
at {}, in {}.
Length:{}

""".format(self.topic, self.description, self.keywords, self.when.strftime("%Y-%m-%d-%H.%M"), self.room, self.duration)
