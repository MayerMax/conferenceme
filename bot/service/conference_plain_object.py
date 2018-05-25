from typing import List


import datetime

import os

from bot.intelligence.photosim import ConferencePhotoModel

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

        self.__sections = {}  # хранит словарь вида имя секции : секция
        for x in self.get_lectures():
            self.__sections[x.section.name] = x.section

        photo_root_dir = self.__conference.root_path
        self.__photo_model = ConferencePhotoModel(img_dir='{}/{}'.format(photo_root_dir, 'speakers'))


    def get_conference_summary(self):
        return self.__conference.__repr__()

    def get_lectures(self) -> List[Lecture]:
        return self.__lectures

    def get_speakers(self) -> List[Speaker]:
        return self.__speakers

    def get_sections(self) -> List[Section]:
        return [x.section for x in self.get_lectures()]


    def get_section_schedule(self, when: datetime.datetime, section_name: str) -> List[Lecture]:
        """
        возвращает список всех лекций данной секции, которые удовлетворяют условию when (конкретно сравнивается месяц,
        день, год)
        :param when: время
        :param section_name: имя секции
        :return: список лекций на это время
        """
        section = self.__sections[section_name]
        return [x for x in section.lectures if x.when.day == when.day and x.when.year == when.year and
                x.when.month == x.when.month]

    def get_speaker_by_photo(self, photo_path: str):
        found_face_path = self.__photo_model.find_relevant_face(photo_path)
        if not found_face_path:
            return None
        found_face_path = os.path.normpath(found_face_path[0])
        # TODO индексация данных для скорости
        return [speaker for speaker in self.__speakers if speaker.photo_path == found_face_path][0]

