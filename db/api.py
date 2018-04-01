"""Модуль api базы данных"""
import db.alchemy as db


class Auth:
    @staticmethod
    def create_organization_account(email, name, password):
        db.Alchemy.get_instance().create_organization_account(email, name, password)

    @staticmethod
    def check_organization_exists(email, password):
        db.Alchemy.get_instance().check_organization_exists(email, password)
