from typing import List

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound

from db.models import Base
from db.models.content import Section, Lecture
from db.models.event import Conference
from db.models.infrastructure import ConferenceHashes
from db.models.official import Organization
from db.models.people import Speaker


class Alchemy:
    db_instance = None

    class __Alchemy:
        def __init__(self, path=''):
            engine = create_engine('sqlite:///{}?check_same_thread=False'.format(path))
            self.__session = scoped_session(sessionmaker(bind=engine))

        def get_session(self):
            return self.__session

        def get_conference_by_id(self, conf_id) -> Conference:
            return self.__session.query(Conference).filter(Conference.id == conf_id).one_or_none()

        def get_conference_speakers(self, conf_id) -> List[Speaker]:
            return self.__session.query(Speaker).filter(Speaker.conf_id == conf_id).all()

        def get_conference_lectures(self, conf_id) -> List[Lecture]:
            return self.__session.query(Lecture).filter(Lecture.conf_id == conf_id).all()

        def get_sections(self, conference_id):
            """
            Возвращает секции конференции по id
            :param conference_id: id конференции
            :return:
            """
            return self.__session.query(Section).filter(Section.conference_id == conference_id).all()

        def get_lections(self, conference_id, section_id, from_date=None, to_date=None):
            """
            Возвращает все лекции во временном промежутке с from_date до to_date, обе даты включаются.
            Если даты не указаны, то возвращаются все лекции данной секции конференции
            :param conference_id: id конференции
            :param section_id: id секции
            :param from_date: нижняя граница лекции по дате
            :param to_date: верхняя граница лекции по дате
            :return:
            """
            if from_date and to_date:
                return self.__session(Lecture).filter(from_date <= Lecture.date <= to_date).all()
            return self.__session(Lecture).filter(Lecture.conference_id == conference_id and
                                                  Lecture.section_id == section_id).all()

        def get_lections_by_date(self, conference_id, section_id, date):
            """
            Сокращение для get_lections, возвращает все лекции в указанный день
            :param conference_id: id конференции
            :param section_id: id секции
            :param date: дата лекции
            :return:
            """
            return self.get_lections(conference_id, section_id, date, date)

        def is_correct_key(self, key):
            """
            Принимает ключ, проверяет, есть ли какая-то конференция с таким клюом,
            Если да - возвращает  True: есть доступ, иначе - False
            :param key: string
            :return: bool
            """
            confhash = self.__session.query(ConferenceHashes) \
                .filter(ConferenceHashes.key == key).one_or_none()
            return confhash

        def check_organization_exists(self, email, password):
            try:
                _ = self.__session.query(Organization).filter(and_(Organization.email_address == email,
                                                                   Organization.password == password)).one()
                return True
            except NoResultFound:
                return False

        def create_organization_account(self, email, name, password):
            try:
                org = Organization(email=email, name=name, password=password)
                self.__session.add(org)
                self.__session.commit()
                return True
            except Exception:
                return False

        def commit_all_data(self, data):
            for d in data:
                if type(d) == list:
                    for piece in d:
                        self.__session.add(piece)
                else:
                    self.__session.add(d)
            self.__session.commit()
            return True

    @staticmethod
    def get_instance(path='data.db'):
        if not Alchemy.db_instance:
            Alchemy.db_instance = Alchemy.__Alchemy(path)

        return Alchemy.db_instance


if __name__ == '__main__':
    a = Alchemy.get_instance()
    s = a.get_session()
    conf = a.get_conference_by_id(1)
    lectures = a.get_conference_lectures(1)
    print([l.when.day for l in lectures])
    # conf_key = ConferenceHashes(1, '12345')
    # s.add(conf_key)
    # s.commit()