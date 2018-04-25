import json
import urllib.request

import jinja2
from flask import Flask, flash
from flask import request, session, redirect, render_template, send_from_directory

from db.alchemy import Alchemy
from db.api import ConferenceApi

app = Flask(__name__)
_ = Alchemy.get_instance('../db/data.db')


@app.route('/send_speaker', methods=['POST'])
def receive_speaker():
    sent_data = request.json
    print(sent_data)


if __name__ == '__main__':
    app.run(host='localhost', port=8080)
