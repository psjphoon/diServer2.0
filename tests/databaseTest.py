import datetime
import requests
import sys
# change path to enable finding the next import
sys.path.append('../')
import dataAnalysis.timeSequenceUtils as tsu


def setupGame(gameID):
    game = {"gameID": gameID}
    resp = requests.post('http://localhost:5000/gameRegistration', json=game)
    if resp.status_code != 201:
        print('registering of game' + str(gameID) + 'failed')
    else:
        print('game registered')

def setupUser(userID):
    user = {"userID": userID}
    resp = requests.post('http://localhost:5000/userRegistration', json=user)
    if resp.status_code != 201:
        print('registering of user' + str(userID) + 'failed')
    else:
        print('user registered')

def send_event(time, data, userID, gameID):
    event = {   "userID": userID, 
                "appID": "dilongGamepad",
                "timestamp": str(time),
                "competition": gameID,
                "event": ''.join(str(buttonPressed) for buttonPressed in data) }
    resp = requests.post('http://localhost:5000/event', json=event)
    if resp.status_code != 201:
        print('sending of event failed')
    else:
        print('Sent ' + str(data))

def main():
    gameID = "testGame"
    users = list((a, a/float(20)) for a in range(1, 6))
    setupGame(gameID)
    realGame = tsu.randomSequenceWithTime(10, 0)
    
    for user in users:
        userID = "tesUser" + str(user[0])
        setupUser(userID)
        userInput = tsu.insertErrorsWithTime(realGame, user[1], 0)
        # the 2 is chosen for no particular reason here
        for event in userInput:
            send_event(event[1], event[0], userID, gameID)
    response = requests.get('http://localhost:5000/game/' + gameID)
    print(response) 
    return
    

if __name__ == '__main__':
  main()
