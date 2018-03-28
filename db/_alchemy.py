import time
from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound

from db._base import User, UserAccessToConference, ConferenceHashes, Base, \
    UserLastActivity, Organization, Conference, Section, Lecture, Speaker


class Alchemy:
    db_instance = None

    class __Alchemy:
        def __init__(self, path=''):
            engine = create_engine('sqlite:///{}'.format(path))
            Base.metadata.bind = engine
            DBSession = sessionmaker(bind=engine)
            self.__session = DBSession()

        def get_session(self):
            return self.__session

        def validate_user(self, user_name):
            """
            Функция валидации пользователя - имеет ли он доступ к опросу бота
            Технически, вызывается всегда, чтобы убедиьться, что пользователь известен боту.
            Далее предполагается, что пользователь предоставит корректный ключ конференции
            :param user_name: уникальное имя пользователя
            :return:
            """
            known_name_id = self.__session.query(User.id) \
                .filter(User.unique_name == user_name).all()
            if not known_name_id:
                return False
            user_id = known_name_id[0]
            has_access = self.__session.query(UserAccessToConference.conference_id) \
                .filter(UserAccessToConference.user_id == user_id).all()
            if has_access:
                return True
            return False

        def get_user_id_by_his_name(self, user_name):
            """
            Возвращает id пользователя по его уникальному имени
            :param user_name: имя пользователя
            :return: int или None
            """
            return self.__session.query(User).filter(User.unique_name == user_name) \
                .one_or_none()

        def enter_user(self, user_name, given_key):
            """
            Осуществляет регистрацию пользователя для последущего обращения к боту за
             информацией по конференции, к которой у него есть доступ
            :param user_name:
            :param given_key:
            :return:
            """
            conference_id_by_key = self.__session.query(ConferenceHashes.conference_id) \
                .filter(ConferenceHashes.key == given_key).one_or_none()
            if not conference_id_by_key:
                return False
            user = self.get_user_id_by_his_name(user_name)
            if not User:
                return False
            new_user_access_rule = UserAccessToConference(user.id, conference_id_by_key)
            new_activity = UserLastActivity(user.id, conference_id_by_key, time.time())
            self.__session.add(new_user_access_rule)
            self.__session.add(new_activity)
            self.__session.commit()
            return True
            # has_user_access = self.__session.query(UserAccessToConference) \
            #     .filter(and_(UserAccessToConference.user_id == user.id,
            #                  UserAccessToConference.conference_id == conference_id_by_key))

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
    def get_instance():
        # TODO: Alchemy and multithreads
        if not Alchemy.db_instance:
            Alchemy.db_instance = Alchemy.__Alchemy()
        else:
            Alchemy.db_instance = Alchemy.__Alchemy()

        return Alchemy.db_instance


if __name__ == '__main__':
    pass
    # s = Alchemy('data.db')
    # s = s.get_session()
    # print(s.query(Speaker.photo_path).all())
