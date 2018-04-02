from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Alchemy:
    db_instance = None

    class __Alchemy:
        def __init__(self, path=''):
            engine = create_engine('sqlite:///{}?check_same_thread=False'.format(path))
            self.__session = scoped_session(sessionmaker(bind=engine))

        def get_session(self):
            return self.__session

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