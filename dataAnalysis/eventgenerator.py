import numpy as np
import pandas as pd
import costMatrixDijkstra as dij
import sequenceUtils as su
import timeSequenceUtils as tsu

from collections import Counter

# to generate same output for examination
np.random.seed(5)

# read input files
stateMachine = pd.read_csv('states.txt', header = None)
stateMachine = stateMachine.fillna(0)
rows, columns = stateMachine.shape

prob = pd.read_csv('probability.txt', header = None)

dKeys = pd.read_csv('keys.txt', header = None)
allKeys = list(dKeys.iloc[0, :])

dErrors = pd.read_csv('errors.txt',index_col='action')

# to generate possible events for each stage
possibleEvents = []
for i in range(columns):
    event = {}
    for j in range(rows):
        if stateMachine.loc[i][j] != 0:
            event.update({stateMachine.loc[i][j]:(j,prob.loc[i][j])})
    possibleEvents.append(event)

# to generate probability
keys = []
probability = []
for i in range(len(possibleEvents)):
    event = []
    prob = []
    for key,value in possibleEvents[i].items():
        event.append(key)
        prob.append(value[1])
    keys.append(event)
    prob = np.asarray(prob)
    prob /= sum(prob)
    probability.append(prob)

# assume first state is always 0
state = 0
sequences = []
userevents = {}
i = state
while state != (rows-1):

    # generate ground truth according to states
    event = np.random.choice(list(possibleEvents[i].keys()),p=probability[i])
    sequences.append(event)

    # generate user inputs based on ground truth
    allKeys = list(dKeys.iloc[0, :])
    allKeys.remove(event)
    if not userevents:
        for user in dErrors:
            change = np.random.choice(['insert', 'delete', 'replace'],p=[dErrors[user]['insert'],dErrors[user]['delete'],1-(dErrors[user]['insert'] + dErrors[user]['delete'])])
            if change == 'insert': 
                userevents[user]=[event]
            elif change == 'replace':
                dividedProb = (1-(dErrors[user]['insert'] + dErrors[user]['delete'])) / len(allKeys)
                replaceProb = [dividedProb] * len(allKeys)
                replaceProb = np.asarray(replaceProb)
                replaceProb /= sum(replaceProb)
                userevents[user]=[np.random.choice(allKeys,p=replaceProb)]
            elif change == 'delete':
                userevents[user]=[]
    else:
        for user in dErrors:
            change = np.random.choice(['insert', 'delete', 'replace'],p=[dErrors[user]['insert'],dErrors[user]['delete'],1-(dErrors[user]['insert'] + dErrors[user]['delete'])])
            if change == 'insert':
                userevents[user].append(event)
            elif change == 'replace':
                dividedProb = (1-(dErrors[user]['insert'] + dErrors[user]['delete'])) / len(allKeys)
                replaceProb = [dividedProb] * len(allKeys)
                replaceProb = np.asarray(replaceProb)
                replaceProb /= sum(replaceProb)
                userevents[user].append(np.random.choice(allKeys,p=replaceProb))

    state=possibleEvents[i][event][0]
    i += (state-i)

userinputs = []
for i in userevents:
    userinputs.append(''.join(userevents[i]))
 
gtruth=''.join(sequences)
path = dij.timeWarpingPathAStar(userinputs)
# TODO determine the states while finding the shortest path
result = su.extractOriginalStates(path, userinputs, possibleEvents)
print(' ')
print('original: ' + gtruth)
print('userInputs: ' + str(userinputs))
print('newGuess: ' + result)
print('new Guess rating: ' + str(dij.sequenceRating(gtruth, result)))
print('userInputs and ratings:')
for s in userinputs:
    rating = dij.sequenceRating(result, s)
    print(s + ": " + str(rating))