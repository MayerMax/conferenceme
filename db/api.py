"""Модуль api базы данных"""
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound

import db.alchemy as db
from db.errors import OrganizationExistsException

from db.models.content import Section, Lecture
from db.models.event import Conference
from db.models.infrastructure import ConferenceHashes
from db.models.official import Organization
from db.models.people import Speaker


class AuthApi:
    @staticmethod
    def create_organization_account(email, name, password):
        session = db.Alchemy.get_instance()

        if AuthApi.check_organization_exists(email, name):
            raise OrganizationExistsException()

        try:
            org = Organization(email=email, name=name, password=password)
            session.add(org)
            session.commit()
            return True
        except Exception:
            return False

    @staticmethod
    def check_organization_exists(email, name):
        session = db.Alchemy.get_instance()
        try:
            _ = session.query(Organization).filter(and_(Organization.email_address == email,
                                                        Organization.name == name)).one()
            return True
        except NoResultFound:
            return False


class ConferenceApi:
    @staticmethod
    def get_conference_by_id(conf_id) -> Conference:
        session = db.Alchemy.get_instance()
        return session.query(Conference).filter(Conference.id == conf_id).one_or_none()

    @staticmethod
    def get_conference_speakers(conf_id) -> List[Speaker]:
        session = db.Alchemy.get_instance()
        return session.query(Speaker).filter(Speaker.conf_id == conf_id).all()

    @staticmethod
    def get_conference_lectures(conf_id) -> List[Lecture]:
        session = db.Alchemy.get_instance()
        return session.query(Lecture).filter(Lecture.conf_id == conf_id).all()

    @staticmethod
    def get_sections(conference_id):
        """
        Возвращает секции конференции по id
        :param conference_id: id конференции
        :return:
        """
        session = db.Alchemy.get_instance()
        return session.query(Section).filter(Section.conference_id == conference_id).all()

    @staticmethod
    def get_lections(conference_id, section_id, from_date=None, to_date=None):
        """
        Возвращает все лекции во временном промежутке с from_date до to_date, обе даты включаются.
        Если даты не указаны, то возвращаются все лекции данной секции конференции
        :param conference_id: id конференции
        :param section_id: id секции
        :param from_date: нижняя граница лекции по дате
        :param to_date: верхняя граница лекции по дате
        :return:
        """
        session = db.Alchemy.get_instance()

        if from_date and to_date:
            return session(Lecture).filter(from_date <= Lecture.date <= to_date).all()
        return session(Lecture).filter(Lecture.conference_id == conference_id and
                                       Lecture.section_id == section_id).all()

    @staticmethod
    def get_lections_by_date(conference_id, section_id, date):
        """
        Сокращение для get_lections, возвращает все лекции в указанный день
        :param conference_id: id конференции
        :param section_id: id секции
        :param date: дата лекции
        :return:
        """
        return ConferenceApi.get_lections(conference_id, section_id, date, date)

    @staticmethod
    def is_correct_key(key):
        """
        Принимает ключ, проверяет, есть ли какая-то конференция с таким клюом,
        Если да - возвращает  True: есть доступ, иначе - False
        :param key: string
        :return: bool
        """
        session = db.Alchemy.get_instance()
        confhash = session.query(ConferenceHashes).filter(ConferenceHashes.key == key).one_or_none()
        return confhash
