from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Organization(Base):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email_address = Column(String)
    password = Column(String)  # no hashes! no salt ! none at all - shit (
    description = Column(String)

    def __init__(self, name, email, password, description=None):
        self.name = name
        self.email_address = email
        self.password = password
        self.description = description

    def __repr__(self):
        return 'Company - {}, about: {}'.format(self.name, self.description)


class Conference(Base):
    __tablename__ = 'conference'
    id = Column(Integer, primary_key=True)
    organization_name = Column(String, ForeignKey('organization.name'))
    name = Column(String)
    begin_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(String)

    sponsors = relationship('Sponsor', backref='conference')
    events = relationship('Event', backref='conference')

    def __init__(self, org_name, name, when_starts, when_ends, location):
        self.organization_name = org_name
        self.name = name
        self.begin_date = when_starts
        self.end_date = when_ends
        self.location = location

    def __repr__(self):
        return 'Conference {}, organized by {}, dates: {} - {}'.format(self.name,
                                                                       self.organization_name,
                                                                       self.begin_date,
                                                                       self.end_date)


class Sponsor(Base):
    __tablename__ = 'sponsor'
    id = Column(Integer, primary_key=True)
    conf_id = Column(Integer, ForeignKey('conference.id'))
    sponsor_name = Column(String, ForeignKey('organization.name'))


class Speaker(Base):
    __tablename__ = 'speaker'
    id = Column(Integer, primary_key=True)
    name = Column(String)  # подразумевается все что угодно в фио или инициалы
    photo_path = Column(String)  # фото профиль
    info = Column(String)

    def __init__(self, name, photo=None, info=None):
        self.name = name
        self.photo_path = photo
        self.info = info

    def __repr__(self):
        return 'Speaker {}, info: {}'.format(self.name, self.info)


class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    conference_id = Column(Integer, ForeignKey('conference.id'))

    lectures = relationship('Lecture', backref='section')

    def __init__(self, name, conference_id):
        self.name = name
        self.conference_id = conference_id

    def __repr__(self):
        return '{}'.format(self.name)


class Lecture(Base):
    __tablename__ = 'lecture'
    id = Column(Integer, primary_key=True)
    speaker_id = Column(Integer, ForeignKey('speaker.id'))
    topic = Column(String)
    about = Column(String)
    date = Column(DateTime)
    duration = Column(Time)
    section_id = Column(Integer, ForeignKey('section.id'))
    conference_id = Column(Integer, ForeignKey('conference.id'))
    location = Column(String)

    def __init__(self, speaker_id, topic, about, when, length, in_section, in_conference, location):
        self.speaker_id = speaker_id
        self.topic = topic
        self.about = about
        self.date = when
        self.duration = length
        self.section_id = in_section
        self.conference_id = in_conference
        self.location = location


class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True)
    conference_id = Column(Integer, ForeignKey('conference.id'))
    event_type = Column(String)
    description = Column(String)
    duration = Column(Time)

    def __init__(self, event_type, about, duration, in_conference):
        self.event_type = event_type
        self.description = about
        self.duration = duration
        self.conference_id = in_conference


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    unique_name = Column(String)
    information = Column(String)

    def __init__(self, name, information=None):
        self.unique_name = name
        self.information = information


class UserAccessToConference(Base):
    __tablename__ = 'access'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    conference_id = Column(Integer, ForeignKey('conference.id'))

    def __init__(self, user_id, conference_id):
        self.user_id = user_id
        self.conference_id = conference_id


class ConferenceHashes(Base):
    __tablename__ = 'hashes'
    conference_id = Column(Integer, ForeignKey('conference.id'))
    key = Column(String, primary_key=True)

    def __init__(self, conf_id, access_key):
        self.conference_id = conf_id
        self.key = access_key


class UserLastActivity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    conference_id = Column(Integer, ForeignKey('conference.id'))
    last_action_time = Column(DateTime)

    def __init__(self, user_id, conference_id, last_time):
        self.user_id = user_id
        self.conference_id = conference_id
        self.last_action_time = last_time


if __name__ == '__main__':
    engine = create_engine('sqlite:///data.db')
    Base.metadata.create_all(engine)
