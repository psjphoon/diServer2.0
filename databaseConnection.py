import pymongo  
from flask import jsonify
import datetime
import dataAnalysis.costMatrixDijkstra as dij
import dataAnalysis.timeSequenceUtils as tsu
import numpy as np

client = pymongo.MongoClient("mongodb://localhost")

diDatabase = client["diDatabase"]

# collections 
competitions = diDatabase["competitions"]
events = diDatabase["events"]
users = diDatabase["users"]
athletes = diDatabase["athletes"]
teams = diDatabase["teams"]
apps = diDatabase["apps"]

def insertGame(document):
      inserting = competitions.find_one(document)
      if inserting != None:
            return False
      else: 
            return diDatabase['competitions'].insert_one(document)

def insertUsers(document):
      inserting = users.find_one(document)
      if inserting != None:
            return False
      else: 
            return diDatabase['users'].insert_one(document)

def insertEvent(event):
      allNecessaryFields = 'userID' in event and 'appID' in event and 'timestamp' in event and 'competition' in event
      if not allNecessaryFields:
            return False
      insertingUser = users.find_one({"userID": event["userID"]})
      if insertingUser == None:
            print(event["userID"] + " is not in databse")
            return False
      events.insert_one(event)
      return True

def insertEvents(events):
      allInsertionsSuccessful = True
      for event in events:
            allInsertionsSuccessful = insertEvent(event) and allInsertionsSuccessful
      return allInsertionsSuccessful

def getCompetitionEvents(gameID):
      competition = competitions.find_one({"gameID": gameID})
      if competition == None:
            print(str(gameID) + " is not in databse")
            return None
      if "events" in competition:
            print("Return game events from database")
            return competition["events"]
      
      # create events from user data
      print("Combine users' data")
      userEvents = {}
      for event in events.find({"competition": gameID}):
            user = event["userID"]
            eventType = event["event"]
            timestamp = event["timestamp"]
            if user in userEvents:
                  userEvents[user].append((eventType, datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')))
            else:
                  userEvents[user] = [(eventType, datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f'))]
      sequences = []
      # choose users
      maxUsersToUse = 5
      annotatingUsers = []
      probability = []
      for user in userEvents.keys():
            dbUser = users.find_one({"userID": user})
            if "rating" in dbUser:
                  annotatingUsers.append((dbUser["rating"], user))
            else:
                  annotatingUsers.append((0.5, user))
                  # since it is normalized, a rating should less than 1
      
      # chooose maxUserTouse number of users according to their probability based on their ratings
      probability = [x[0] for x in annotatingUsers]
      probability = np.array(probability)  
      probability /= sum(probability)   # to normalize
      ranking = [x[1] for x in annotatingUsers]
      ranking = np.random.choice(np.asarray(ranking), size=maxUsersToUse, replace=False, p=probability)
      annotatingUsers = [tuple for x in ranking for tuple in annotatingUsers if tuple[1] == x] 

      for ratedUser in annotatingUsers:
            sequences.append(userEvents[ratedUser[1]])
      path = dij.aStarTimeWarpingPathWithTimestamps(sequences)
      resultSequence = tsu.extractOriginalWithTime(path, sequences)
      '''
      resultSequence = [('a', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('b', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('c', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), 
        ('d', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('e', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 49, 356759))]
      
      resultSequence = [('a', datetime.datetime(2019, 10, 24, 12, 5, 50, 356759)), ('b', datetime.datetime(2019, 10, 24, 12, 5, 51, 356759)), ('c', datetime.datetime(2019, 10, 24, 12, 5, 52, 356759)), 
        ('d', datetime.datetime(2019, 10, 24, 12, 5, 53, 356759)), ('e', datetime.datetime(2019, 10, 24, 12, 5, 54, 356759)), ('f', datetime.datetime(2019, 10, 24, 12, 5, 55, 356759))]
      '''
      # add result events to game document
      jsonSequence = list({"event": str(s[0]), "timestamp":str(s[1])} for s in resultSequence)
      competitions.update_one({"_id": competition["_id"]}, {"$set": {"events": jsonSequence}})

      # update user annotating scores
      for user in userEvents.keys():
            dbUser = users.find_one({"userID": user})
            thisGameRating = dij.sequenceRatingWithTime(resultSequence, userEvents[user])
            newRating = 0.0
            gamesAnnotated = 0.0
            alpha = 0.2
            games = 0
            avgRating = 0

            if "rating" in dbUser:
                  # if a rating exists, a number of annotated games should also be there
                  gamesAnnotated = dbUser["gamesAnnotated"]
                  currentRating = dbUser["rating"]
                  games = dbUser["games"]
                  avgRating = dbUser["averageRating"]
                  #newRating = (gamesAnnotated * currentRating + thisGameRating)/(gamesAnnotated + 1)
                  newRating = alpha * currentRating + (1-alpha) * thisGameRating
                  games += 1
                  #print(str(user) + " user rating: " + str(newRating))
            else:
                  newRating = thisGameRating
                  games += 1
                  #print(str(user) + " user rating: " + str(newRating))
            if user in ranking:
                  gamesAnnotated += 1
            users.update_one({"_id": dbUser["_id"]}, {"$set": {"rating": newRating, "gamesAnnotated": gamesAnnotated, "games":games, "averageRating":avgRating}})   

      for user in userEvents.keys():
            dbUser = users.find_one({"userID": user})
            oldAvgRating = dbUser["averageRating"]
            currentRating = dbUser["rating"]
            games = dbUser["games"]
            avgRating = ((oldAvgRating * (games-1)) + currentRating)/games
            users.update_one({"_id": dbUser["_id"]}, {"$set": {"averageRating":avgRating}})   

      return jsonSequence 