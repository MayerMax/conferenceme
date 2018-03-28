import base64
import os
import random
from datetime import datetime
import timestring
from db._base import Conference, Speaker, Lecture, Section


class TempRelationalObject:
    def __init__(self, json_response):
        self.conference = Conference(org_name=json_response.get('org'),
                                     name=json_response.get('title'),
                                     when_starts=timestring.Date(json_response.get('start')).date,
                                     when_ends=timestring.Date(json_response.get('end')).date,
                                     location=None)
        self.sections = []
        self.lectures = []
        self.speakers = []

    def create_section(self, section_description):
        section = Section(
            name=section_description['section'],
            conference_id=self.conference.id
        )
        self.sections.append(section)
        raw_lectures = section_description['lectures']
        for raw_lecture in raw_lectures:
            self.lectures.append(self.create_lecture(raw_lecture, section.id))

    def create_lecture(self, lecture_info_json, section_id):
        data = lecture_info_json
        speaker_name, speaker_info, about, src = data['speakerName'], data['speakerInfo'], \
                                                 data['lectureAbout'], data['photo']

        speaker = self.make_speaker(self.conference.name, speaker_name, speaker_info, src)
        lecture = Lecture(
            speaker_id=speaker.id,
            topic=about,  # ?
            about=about,
            when=None,
            length=None,
            in_section=section_id,
            in_conference=self.conference.id,
            location=None)
        return lecture

    def make_speaker(self, conf_name, name, info, photo):
        if not os.path.exists('conferences/{}'.format(conf_name)):
            os.makedirs('conferences/{}'.format(conf_name))
        random_name = ''.join(random.choice('0123456789ABCDEF') for _ in range(16))
        path = 'conferences/{}/{}.{}'.format(conf_name, random_name, 'jpeg')
        with open(path, 'wb') as f:
            f.write(base64.b64decode(photo[23:]))

        speaker = Speaker(name=name, info=info, photo=path)
        self.speakers.append(speaker)
        return speaker

    def get_data_for_commit(self):
        return [self.conference, self.speakers, self.sections, self.lectures]