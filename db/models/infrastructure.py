from sqlalchemy import Column, Integer, String, ForeignKey

from db.models import Base


class ConferenceHashes(Base):
    __tablename__ = 'hashes'
    conf_id = Column(Integer, ForeignKey('conference.id'))
    key = Column(String, primary_key=True)

    def __init__(self, conf_id, access_key):
        self.conf_id = conf_id
        self.key = access_key
