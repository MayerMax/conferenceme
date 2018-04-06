from typing import List

from db.models.content import Lecture, Section
from db.models.event import Conference
from db.models.people import Speaker


class ConferencePlainObject:
    """
    класс, который представляет собой выгруженную конференцию, поддерживает базовые запросы к информации:
    найти имя, найти лекцию, упорядочить лекции по дате и так далее
    """

    def __init__(self, conference_general: Conference, speakers: List[Speaker], lectures: List[Lecture]):
        """
        конструктор
        :param conference_general: выгруженный объект Conference
        :param speakers: выгруженный список спикеров
        :param lectures: выгруженный список лекций
        """
        self.__conference = conference_general
        self.__speakers = speakers
        self.__lectures = lectures

    def get_conference_summary(self):
        return self.__conference.__repr__()

    def get_lectures(self) -> List[Lecture]:
        return self.__lectures

    def get_speakers(self) -> List[Speaker]:
        return self.__speakers

    def get_sections(self) -> List[Section]:
        return [x.section for x in self.get_lectures()]