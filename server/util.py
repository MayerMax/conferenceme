from datetime import datetime
from typing import Dict
from db.models.content import Lecture
from db.models.event import Conference
from db.models.people import Speaker
from db.api import ConferenceApi


class DictForJson:
    DATETIME_FORMAT = '%Y %m %d %H:%M:%S'

    @staticmethod
    def to_conference_dict(json: Dict[str, object], default=None) -> Dict[str, str]:
        return {
            'id': int(json['id']),
            'name': json['name'],
            'conference_topics': json['topics'],
            'begin_date': datetime.strptime(json['begin_date'],
                                            DictForJson.DATETIME_FORMAT),
            'end_date': datetime.strptime(json['end_date'],
                                          DictForJson.DATETIME_FORMAT)
        } if json else default

    @staticmethod
    def to_lecture_dict(json: Dict[str, object], default=None) -> Dict[str, str]:
        return {
            'id': int(json['id']),
            'conf_id': int(json['conference_id']),
            'topic': json['topic'],
            'description': json['about'],
            'when': datetime.strptime(json['date'],
                                      DictForJson.DATETIME_FORMAT),
            'duration': json['duration'],
            'tags': ';'.join(json['tagsLecture']),
            'room': json['hallLecture'],
            'photo': json['photo'],
        } if json else default

    @staticmethod
    def to_speaker_dict(json: Dict[str, object], default=None) -> Dict[str, str]:
        return {
            'id': int(json['id']),
            'conf_id': int(json['conference_id']),
            'lecture_id': int(json['lection_id']),
            'description': json['info'],
            'tags': ';'.join(json['tagsSpeaker']),
            'external_links': ';'.join(json['link']),
            'photo': json['photo'],
            'first_name': json['name'],
            'surname': json['surName'],
            'middle_name': json['otchestvo'],
            'science_degree': json['profession'],
        } if json else default

    @staticmethod
    def from_conference(conference: Conference, default=None):
        return {
            'id': conference.id,
            'name': conference.name,
            'topics': conference.conference_topics,
            'begin_date': conference.begin_date.strftime(DictForJson.DATETIME_FORMAT),
            'end_date': conference.end_date.strftime(DictForJson.DATETIME_FORMAT),
            'location': 'location stub',
            'sections': None,
            'lectures': [DictForJson.from_lecture(lecture)
                         for lecture in ConferenceApi.get_conference_lectures(conference.id)],
            'speakers': [DictForJson.from_speaker(speaker)
                         for speaker in ConferenceApi.get_conference_speakers(conference.id)]
        } if conference else default

    @staticmethod
    def from_conference_light(conference: Conference, default=None):
        return {
            'id': conference.id,
            'name': conference.name,
            'topics': conference.conference_topics,
            'begin_date': conference.begin_date.strftime(DictForJson.DATETIME_FORMAT),
            'end_date': conference.end_date.strftime(DictForJson.DATETIME_FORMAT),
            'location': 'location stub',
            'sections': None,
            'lectures': None,
            'speakers': None
        } if conference else default

    @staticmethod
    def from_lecture(lecture: Lecture, default=None):
        return {
            'conference_id': lecture.conf_id,
            'id': lecture.id,
            'topic': lecture.topic,
            'about': lecture.description,
            'date': lecture.when.strftime(DictForJson.DATETIME_FORMAT),
            'duration': lecture.duration,
            'tagsLecture': [x.strip() for x in lecture.tags.split(';')],
            'hallLecture': lecture.room,
            'files': None,
            'photo': lecture.photo
        } if lecture else default

    @staticmethod
    def from_speaker(speaker: Speaker, default=None):
        return {
            'conference_id': speaker.conf_id,
            'lection_id': speaker.lecture_id,
            'id': speaker.id,
            'tagsSpeaker': [x.strip() for x in speaker.tags.split(';')],
            'link': [x.strip() for x in speaker.external_links.split(';')],

            'photo': speaker.photo,
            'name': speaker.first_name,
            'surName': speaker.surname,
            'otchestvo': speaker.middle_name,
            'info': speaker.description,
            'profession': speaker.science_degree
        } if speaker else default



