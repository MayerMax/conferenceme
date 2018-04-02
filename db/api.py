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
