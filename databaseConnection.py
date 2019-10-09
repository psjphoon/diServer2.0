import pymongo  
from flask import jsonify
import datetime
import dataAnalysis.costMatrixDijkstra as dij
import dataAnalysis.timeSequenceUtils as tsu

client = pymongo.MongoClient("mongodb://localhost")

diDatabase = client["diDatabase"]

# collections 
competitions = diDatabase["competitions"]
athletes = diDatabase["athletes"]
teams = diDatabase["teams"]
events = diDatabase["events"]
users = diDatabase["users"]
apps = diDatabase["apps"]

def insertEvent(event):
      allNecessaryFields = 'userID' in event and 'appID' in event and 'timestamp' in event and 'competition' in event
      if not allNecessaryFields:
            return False
      insertingUser = users.find_one({"userID": event["userID"]})
      if insertingUser == None:
            print(event["userID"] + " is not in databse")
            return False
      events.insert_one(event)
      print("event insterted")
      return True

def insertEvents(events):
      allInsertionsSuccessful = True
      for event in events:
            allInsertionsSuccessful = insertEvent(event) and allInsertionsSuccessful
      return allInsertionsSuccessful

def insertIntoCollection(collectionName, document):
      if collectionName == "events":
            return insertEvent(document)
      else: 
            return diDatabase[collectionName].insert_one(document)

def getCompetitionEvents(gameID):
      competition = competitions.find_one({"gameID": gameID})
      if competition == None:
            print(str(gameID) + " is not in databse")
            return None
      if "events" in competition:
            print("return game events from database")
            return competition["events"]
      # create events from user data
      print("combine user data")
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
      maxUsersToUse = 4
      annotatingUsers = []
      for user in userEvents.keys():
            dbUser = users.find_one({"userID": user})
            if "rating" in dbUser:
                  annotatingUsers.append((dbUser["rating"], user))
            else:
                  annotatingUsers.append((2.0, user))
                  # since it is normalized, a rating should get worse than 1

      if len(annotatingUsers) > maxUsersToUse:
            annotatingUsers.sort()
            annotatingUsers = annotatingUsers[:maxUsersToUse]

      for ratedUser in annotatingUsers:
            sequences.append(userEvents[ratedUser[1]])
      path = dij.aStarTimeWarpingPathWithTimestamps(sequences)
      resultSequence = tsu.extractOriginalWithTime(path, sequences)
      # add result events to game document
      jsonSequence = list({"event": str(s[0]), "timestamp":str(s[1])} for s in resultSequence)
      competitions.update_one({"_id": competition["_id"]}, {"$set": {"events": jsonSequence}})

      # update user annotating scores
      # TODO : Test this somehow
      for user in userEvents.keys():
            dbUser = users.find_one({"userID": user})
            thisGameRating = dij.sequenceRatingWithTime(resultSequence, userEvents[user])
            newRating = 0.0
            gamesAnnotated = 1.0
            if "rating" in dbUser:
                  # if a rating exists, a number of annotated games should also be there
                  gamesAnnotated = dbUser["gamesAnnotated"]
                  currentRating = dbUser["rating"]
                  newRating = (gamesAnnotated * currentRating + thisGameRating)/(gamesAnnotated + 1)
                  gamesAnnotated += dbUser["gamesAnnotated"]
                  print(str(user) + " user rating: " + str(newRating))
            else:
                  newRating = thisGameRating
            users.update_one({"_id": dbUser["_id"]}, {"$set": {"rating": newRating, "gamesAnnotated": gamesAnnotated}})

      return jsonSequence 