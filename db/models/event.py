from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db.models import Base


class Conference(Base):
    __tablename__ = 'conference'
    id = Column(Integer, primary_key=True)
    organization_name = Column(String, ForeignKey('organization.name'))
    conference_topics = Column(String)
    name = Column(String)
    begin_date = Column(DateTime)
    end_date = Column(DateTime)
    logo_path = Column(String)
    external_links = Column(String)
    root_path = Column(String)
    org = relationship('Organization', backref='conferences')

    def __repr__(self):
        return """
You are on the {} conference,
Topics will be discussed: {}
Dates {} - {},
Our links: {}
        """.format(self.name, self.conference_topics, self.begin_date, self.end_date, self.external_links)


class RestActivity(Base):
    __tablename__ = 'rest'
    id = Column(Integer, primary_key=True)
    conference_id = Column(Integer, ForeignKey('conference.id'))
    activity_type = Column(String)
    place = Column(String)
    time = Column(String)  # ?
    description = Column(String)

    conference = relationship('Conference', backref='rest_activities')


class ActualObject(Base):
    __tablename__ = 'actual'
    id = Column(Integer, primary_key=True)
