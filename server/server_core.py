from flask import request, jsonify, Flask
from flask_jwt_extended import (JWTManager, jwt_required, jwt_refresh_token_required,
                                create_access_token, create_refresh_token, get_jwt_identity)

from db.alchemy import Alchemy
from db.api import AuthApi
from db.errors import OrganizationExistsException
from server.keys import APP_SECRET_KEY, JWT_SECRET_KEY

app = Flask(__name__)
app.secret_key = APP_SECRET_KEY
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)


@app.route('/register', methods=['POST'])
def register():
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), 400
    data = request.json
    missing_params_msg = find_missing_json_params(data, 'email', 'password', 'org_name')
    if missing_params_msg:
        return jsonify({'msg': missing_params_msg}), 400
    email, password, org_name = data['email'], data['password'], data['org_name']
    try:
        AuthApi.create_organization_account(email, org_name, password)
        status = True
    except OrganizationExistsException:
        status = False
    return jsonify(result=status), 200


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), 400
    data = request.json
    missing_params_msg = find_missing_json_params(data, 'email', 'password')
    if missing_params_msg:
        return jsonify({'msg': missing_params_msg}), 400
    email, password = data['email'], data['password']
    if not AuthApi.check_organization_exists(email, password):
        return jsonify(msg='Incorrect email or password', status=False), 401

    access_token = create_access_token(identity=email)
    refresh_token = create_refresh_token(identity=email)
    return jsonify(access_token=access_token, refresh_token=refresh_token, status=True), 200


@app.route('/refresh_token', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    return jsonify(access_token=create_access_token(identity=get_jwt_identity())), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify(identity=get_jwt_identity()), 200


def find_missing_json_params(json_data, *params):
    for parameter in params:
        if not parameter in json_data:
            return 'Missing {} parameter'.format(parameter)


if __name__ == '__main__':
    _ = Alchemy.get_instance('../db/data.db')
    app.run(debug=True)
