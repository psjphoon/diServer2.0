from flask import (jsonify, Blueprint, request)
import databaseConnection as db

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/appRegistration', methods=['POST'])
def register_app():
    # TODO
    return None

@admin_api.route('/gameRegistration', methods=['POST'])
def register_game():
    if not request.json:
        return jsonify({'status' : True, 'message':'Wrong document type'}), 400
    dbEntry = db.insertGame(request.json)
    if not dbEntry:
        return jsonify({'status' : True, 'message':'Game has registered previously'}), 201
    return jsonify({'status': True, 'message': 'Game insertion successful', 'gameid': str(dbEntry.inserted_id)}), 201

@admin_api.route('/userRegistration', methods=['POST'])
def register_user():
    # TODO
    if not request.json:
        return jsonify({'status' : True, 'message':'Wrong document type'}), 400
    dbEntry = db.insertUsers(request.json)
    if not dbEntry:
        return jsonify({'status' : True, 'message':'User has registered previously'}), 201
    return jsonify({'status': True, 'message': 'User insertion successful', 'userid': str(dbEntry.inserted_id)}), 201

@admin_api.route('/playerRegistration', methods=['POST'])
def register_player():
    # TODO
    return None

@admin_api.route('/teamRegistration', methods=['POST'])
def register_team():
    # TODO
    return None

@admin_api.route('/seasonRegistration', methods=['POST'])
def register_season():
    # TODO
    return None