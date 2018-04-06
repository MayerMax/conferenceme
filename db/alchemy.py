import os
import stat
from db.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Alchemy:
    db_instance = None

    class __Alchemy:
        def __init__(self, path, engine=None):
            """Обертка над существующей базой данных

            :param path: путь до существующей sqlite-бд
            """
            self._path = path
            if engine:
                self.__engine = engine
            else:
                self.__engine = create_engine('sqlite:///{}'.format(path))

            self.__session = scoped_session(sessionmaker(bind=self.__engine))

            # for mode in [stat.S_IRUSR, stat.S_IWUSR,
            #              stat.S_IRGRP, stat.S_IWGRP,
            #              stat.S_IROTH, stat.S_IWOTH]:
            #     os.chmod(path, mode)

        def get_engine(self):
            return self.__engine

        def get_session(self):
            return self.__session()

        def commit_all_data(self, data):
            session = self.get_session()

            for d in data:
                if type(d) == list:
                    for piece in d:
                        session.add(piece)
                else:
                    session.add(d)

            session.commit()
            return True

    @staticmethod
    def get_instance(path='data.db'):
        if not Alchemy.db_instance:
            Alchemy.db_instance = Alchemy.__Alchemy(path)

        return Alchemy.db_instance

    @staticmethod
    def get_session(path='data.db'):
        return Alchemy.get_instance(path).get_session()

    @staticmethod
    def init_with_engine(path, engine):
        Alchemy.db_instance = Alchemy.__Alchemy(path, engine)
        return Alchemy.db_instance


if __name__ == '__main__':
    s = Alchemy.get_instance().get_session()
    # conf_key = ConferenceHashes(1, '12345')
    # s.add(conf_key)
    # s.commit()
