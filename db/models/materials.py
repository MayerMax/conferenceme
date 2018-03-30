from sqlalchemy import Column, Integer, String, ForeignKey

from db.models import Base


class LectureMaterials(Base):
    __tablename__ = 'materials'
    id = Column(Integer, primary_key=True)
    lecture_id = Column(Integer, ForeignKey('lecture.id'))
    name = Column(String)
    tags = Column(String)
    file_path = Column(String)
    description = Column(String)