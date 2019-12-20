import datetime
import requests
import sys
# change path to enable finding the next import
sys.path.append('../')
import dataAnalysis.timeSequenceUtils as tsu


def setupGame(gameID):
    game = {"gameID": gameID}
    print('')
    print('> Register game ' + str(gameID))
    resp = requests.post('http://localhost:5000/gameRegistration', json=game)
    if resp.status_code != 201:
        print(resp.json()['message'])
    else:
        print(resp.json()['message'])

def setupUser(userID):
    user = {"userID": userID}
    print('')
    print('> Register user ' + str(userID))
    resp = requests.post('http://localhost:5000/userRegistration', json=user)
    if resp.status_code != 201:
        print(resp.json()['message'])
    else:
        print(resp.json()['message'])


def send_event(time, data, userID, gameID):
    event = {   "userID": userID, 
                "appID": "dilongGamepad",
                "timestamp": str(time),
                "competition": gameID,
                "event": ''.join(str(buttonPressed) for buttonPressed in data) }
    resp = requests.post('http://localhost:5000/event', json=event)
    if resp.status_code != 201:
        print(resp.json()['message'])
    else:
        print('> Send ' + str(data) + ' @ ' + str(time))
        print(resp.json()['message'])
        

def main():
    # create and register game
    games = list(a for a in range(1,11))
    for game in games:
        gameID = "Game " + str(game)
        setupGame(gameID)

        gTruth = tsu.randomSequenceWithTime(5, 3)	# create event with time difference (no.OfEvents, avgSecBetweenEvents)
        #gTruth = [('a', datetime.datetime(2019, 10, 24, 12, 5, 50, 356759)), ('b', datetime.datetime(2019, 10, 24, 12, 5, 51, 356759)), ('c', datetime.datetime(2019, 10, 24, 12, 5, 52, 356759)), 
        #('d', datetime.datetime(2019, 10, 24, 12, 5, 53, 356759)), ('e', datetime.datetime(2019, 10, 24, 12, 5, 54, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 55, 356759))]

        # create and register users with userInput then send event
        #users = list((b, b/float(20)) for b in range(1, 6)) 
        users = [(1,0.1), (2,0.1), (3,0.1), (4,0.1), (5,0.1), (6,0.2), (7,0.2), (8,0.2), (9,0.3), (10,0.3)]
        '''
        usersinputs = [[('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('b', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('c', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)),
         ('d', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('e', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759))],

         [('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('b', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('c', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)),
         ('d', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('e', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759))],
        
         [('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)),
         ('d', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('e', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759))],
       
         [('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)),
         ('d', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('e', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759))],
      
         [('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)),
         ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759))]]
        '''
        i=0
        for user in users:
            # register user
            userID = "User " + str(user[0])
            setupUser(userID) 

            # create userInput from gTruth
            userInput = tsu.insertErrorsWithTime(gTruth, user[1], 1.5) # (events, errorProbability, maxTimeErrorInSecs)
            #userInput = usersinputs[i]

            # send event
            print('> Start sending events')
            for event in userInput:
                send_event(event[1], event[0], userID, gameID) # (time, data, userID, gameID)

            i+=1

        print('')
        print('> Get combined game events')
        response = requests.get('http://localhost:5000/game/' + gameID)
        data = response.json()
        for event in data:
            print(event['event'] + ' @ ' + event['timestamp'])

        



if __name__ == '__main__':
  main()
