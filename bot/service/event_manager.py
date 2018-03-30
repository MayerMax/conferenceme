
from bot.service.conference_plain_object import ConferencePlainObject
from db.alchemy import Alchemy


class AlreadyExistConference(Exception):
    pass


class NoSuchConferenceLoaded(Exception):
    pass


class EventManager:
    def __init__(self, alchemy: Alchemy = None):
        """
        класс, который хранит в себе выгруженные конференции
        :param alchemy: класс алхимии или None, тогда создастся свое подключение
        """
        self.__loaded_conferences = {}
        if alchemy:
            self.alchemy = alchemy
        else:
            self.alchemy = Alchemy('../../db/data.db')

    def load_conference(self, conf_id: int) -> ConferencePlainObject:
        """
        загружает конференцию по выбранному id.
        если конференция уже выгружена - кидает исключение
        :param conf_id: id конференции
        :return: ConferencePlainObject
        """
        if conf_id in self.__loaded_conferences:
            raise AlreadyExistConference('Conference by this id - {} already exists'.format(conf_id))
        cpo = ConferencePlainObject(self.alchemy.get_conference_by_id(conf_id),
                                    self.alchemy.get_conference_speakers(conf_id),
                                    self.alchemy.get_conference_lectures(conf_id))
        self.__loaded_conferences[conf_id] = cpo
        return cpo

    def pop_conference(self, conf_id: int):
        """
        удаляет конференцию из памяти, в случае неудачи - кидает исклчение
        :param conf_id: id выгруженной конференции
        :return: None
        """
        if conf_id not in self.__loaded_conferences:
            raise NoSuchConferenceLoaded('Can not delete this conference, as it does not exist')
        self.__loaded_conferences.pop(conf_id)


if __name__ == '__main__':
    em = EventManager()
    cpo = em.load_conference(1)
    print(cpo.get_conference_summary())
    em.pop_conference(1)
