from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.models import Base


class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey('conference.id'))
    name = Column(String)
    email = Column(String)
    external_links = Column(String)
    phone = Column(String)
    duty = Column(String)
    photo_path = Column(String)
    conf = relationship('Conference', backref='contacts')


class Face(Base):
    __tablename__ = 'face'
    id = Column(Integer, primary_key=True)
    org_id = Column(Integer, ForeignKey('organization.id'))
    name = Column(String)
    email_address = Column(String)
    external_links = Column(String)
    duty = Column(String)
    description = Column(String)
    photo_path = Column(String)


class Speaker(Base):
    __tablename__ = 'speaker'
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('lecture.id'))
    conf_id = Column(Integer, ForeignKey('conference.id'))
    name = Column(String)
    description = Column(String)
    tags = Column(String)
    external_links = Column(String)
    science_degree = Column(String)
    photo_path = Column(String)

    lecture = relationship('Lecture', backref='speakers')
    conference = relationship('Conference', backref='speakers')

    def __repr__(self):
        return """
This is {}.
What I know about the speaker: {},
Speaker's science degree is:{},
You can learn more using links {}""".format(self.name, self.description, self.science_degree, self.external_links)

    @staticmethod
    def convert_raw_data_to_speaker(speaker_data: dict):
        data = speaker_data
        s = Speaker(
            lecture_id=data['lecture_id'],
            conf_id = data['']
        )

class Visitor(Base):
    __tablename__ = 'visitor'
    id = Column(Integer, primary_key=True)
    conf_id = Column(Integer, ForeignKey('conference.id'))
    name = Column(String)
    description = Column(String)
    external_links = Column(String)
    photo_path = Column(String)
