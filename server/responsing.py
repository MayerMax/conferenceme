import json
import os
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

from db.alchemy import Alchemy
from db.api import ConferenceApi, SpeakerApi, LectureApi
from server.util import DictForJson
from db.tests._create import create_db


app = Flask(__name__)
CORS(app)
_ = Alchemy.get_instance('../db/data.db')


@app.route('/conference/<int:conference_id>', methods=['GET'])
def send_conference(conference_id):
    conference = ConferenceApi.get_conference(conference_id)
    response = DictForJson.from_conference(conference)
    return jsonify(response), 200


@app.route('/lecture/<int:lecture_id>', methods=['GET'])
def send_lecture(lecture_id):
    lecture = LectureApi.get_lecture(lecture_id)
    response = DictForJson.from_lecture(lecture)
    return jsonify(response), 200


@app.route('/speaker/<int:speaker_id>', methods=['GET'])
def send_speaker(speaker_id):
    speaker = SpeakerApi.get_speaker(speaker_id)
    response = DictForJson.from_speaker(speaker)
    return jsonify(response), 200


@app.route('/all_conferences', methods=['GET'])
def send_all_conferences():
    conferences = ConferenceApi.get_all_conferences()
    response = [DictForJson.from_conference_light(conference)
                for conference in conferences]

    return jsonify(response), 200


@app.route('/new_conference', methods=['GET'])
def send_new_conference_id():
    return jsonify(ConferenceApi.create_empty_conference()), 200


@app.route('/conference', methods=['POST'])
def receive_speaker():
    received_data = request.json

    result = True
    if received_data:
        conference = DictForJson.to_conference_dict(received_data)

        lectures = [DictForJson.to_lecture_dict(lecture_json)
                    for lecture_json in received_data['lectures']] if received_data['lectures'] else None

        speakers = [DictForJson.to_speaker_dict(speaker_json)
                    for speaker_json in received_data['speakers']] if received_data['speakers'] else None

        result &= ConferenceApi.update_conference(conference)
        result &= LectureApi.update_lectures(lectures)
        result &= SpeakerApi.update_speakers(speakers)

    return json.dumps({'OK': 200} if result else {'Internal Server Error': 500})


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
