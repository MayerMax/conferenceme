import json
import urllib.request

import jinja2
from flask import Flask, flash
from flask import request, session, redirect, render_template, send_from_directory
from flask_cors import CORS, cross_origin

from db.alchemy import Alchemy
from db.api import ConferenceApi

app = Flask(__name__)
CORS(app)
_ = Alchemy.get_instance('../db/data.db')


@app.route('/Speaker', methods=['POST'])
def receive_speaker():
    sent_data = request.json
    print(sent_data)
    return json.dumps({'ok': 200})


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
