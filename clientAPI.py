from flask import (jsonify, Blueprint, request)
import databaseConnection as db

client_api = Blueprint('client_api', __name__)

@client_api.route('/event', methods=['POST'])
def add_event():
    print("got event")
    if not request.json:
        return jsonify({'status' : 'True', 'message':'Wrong document type'}), 400
    success = db.insertEvent(request.json)
    if not success:
        print("not all fields")
        return jsonify({'status' : 'True', 'message':'Insertion not successful'}), 400
    return jsonify({'status' : 'True', 'message':'Insertion successful'}), 201

@client_api.route('/user/auth', methods=['POST'])
def authenticate_user():
    # TODO
    return None

@client_api.route('/app/auth', methods=['POST'])
def authenticate_app():
    # TODO
    return None

@client_api.route('/team/<teamid>', methods=['GET'])
def get_team_info(teamid):
    # TODO
    return None

@client_api.route('/game/<gameid>', methods=['GET'])
def get_game_info(gameid):
    # TODO: Change to fit API specification
    print("got event")
    events = db.getCompetitionEvents(gameid)
    if events == None:
        print("error in retrieving data")
        return jsonify({'status' : 'True', 'message':'No data for this game'}), 400
    print("found something, sending it back now")
    print(events)
    return jsonify(events), 201

@client_api.route('/player/<playerid>', methods=['GET'])
def get_player_info(playerid):
    # TODO
    return None

@client_api.route('/season/<teamid>', methods=['GET'])
def get_season_info(userid):
    # TODO
    return None

@client_api.route('/statistics/<playerid>|<gameid>|<seasonid>', methods=['GET'])
def get_statistics(playerid, gameid, seasonid):
    # TODO
    return None