import datetime

from bot.service.conference_plain_object import ConferencePlainObject
from db.alchemy import Alchemy
from db.api import ConferenceApi


class AlreadyExistConference(Exception):
    pass


class NoSuchConferenceLoaded(Exception):
    pass


class EventManager:
    def __init__(self):
        """
        класс, который хранит в себе выгруженные конференции
        :param conf_api: класс алхимии или None, тогда создастся свое подключение
        """
        self.__loaded_conferences = {}

    def load_conference(self, conf_id: int) -> ConferencePlainObject:
        """
        загружает конференцию по выбранному id.
        если конференция уже выгружена - кидает исключение
        :param conf_id: id конференции
        :return: ConferencePlainObject
        """
        if conf_id in self.__loaded_conferences:
            raise AlreadyExistConference('Conference by this id - {} already exists'.format(conf_id))
        cpo = ConferencePlainObject(ConferenceApi.get_conference_by_id(conf_id),
                                    ConferenceApi.get_conference_speakers(conf_id),
                                    ConferenceApi.get_conference_lectures(conf_id))
        self.__loaded_conferences[conf_id] = cpo
        return cpo

    def pop_conference(self, conf_id: int):
        """
        удаляет конференцию из памяти, в случае неудачи - кидает исклчение
        :param conf_id: id выгруженной конференции
        :return: None
        """
        if conf_id not in self.__loaded_conferences:
            raise NoSuchConferenceLoaded('Can not load this conference, as it does not exist')
        self.__loaded_conferences.pop(conf_id)

    def get_conference(self, conf_id: int) -> ConferencePlainObject:
        if conf_id not in self.__loaded_conferences:
            raise NoSuchConferenceLoaded('Can not load this conference, as it does not exist')
        return self.__loaded_conferences.get(conf_id)


if __name__ == '__main__':
    a = Alchemy.get_instance('../../db/data.db')
    em = EventManager()
    cpo = em.load_conference(1)
    # print(cpo.get_conference_summary())
    # em.pop_conference(1)
    today = datetime.datetime.now() + datetime.timedelta(days=1)
    print(cpo.get_section_schedule(today, 'It in modern life'))