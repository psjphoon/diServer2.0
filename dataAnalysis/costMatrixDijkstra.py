import datetime
import heapq
import math
from itertools import permutations

# turn into global variables to prevent excessive copying
allDirections = []
sequences = []

def distHeuristic(indices):
    global sequences
    stepsLeft = list(len(sequences[i]) - indices[i] for i in range(len(sequences)))
    maxLeft = max(stepsLeft)
    spaces = 0
    for sl in stepsLeft:
        spaces += maxLeft - sl
        
    return spaces

def charDist(indices):
    global sequences
    chars = set(sequences[i][indices[i]] for i in range(len(sequences)))
    return len(chars) - 1

def charDistWithTime(indices):
    global sequences
    chars = set(sequences[i][indices[i]][0] for i in range(len(sequences)))
    return len(chars) - 1

def spaceDist(lastPosition, nextPosition):
    global sequences
    charList = list(sequences[i][nextPosition[i]] for i in range(len(sequences)) if nextPosition[i] > lastPosition[i])
    spaces = len(sequences) - len(charList)
    return len(set(charList)) - 1 + spaces

def spaceDistWithTime(lastPosition, nextPosition):
    global sequences
    charList = list(sequences[i][nextPosition[i]][0] for i in range(len(sequences)) if nextPosition[i] > lastPosition[i])
    spaces = len(sequences) - len(charList)
    return len(set(charList)) - 1 + spaces

def averageTime(timestamps):
    referenceTS = timestamps[0]
    allDists = datetime.timedelta(0,0)
    for ts in timestamps:
        allDists += ts - referenceTS
    averageTime = referenceTS + allDists/len(timestamps)
    return averageTime

def standardDeviation(timestamps):
    avTime = averageTime(timestamps)
    standardDevInSecs = 0
    for ts in timestamps:
        timeDiff = ts - avTime
        standardDevInSecs += math.pow(timeDiff.total_seconds(), 2)
    standardDevInSecs /= len(timestamps)
    #return datetime.timedelta(0, standardDevInSecs)
    return standardDevInSecs

def withTimeDist(lastPosition, nextPosition, noMatchTimePenalty):
    global sequences
    eventDist = spaceDistWithTime(lastPosition, nextPosition)
    timestamps = list(sequences[i][nextPosition[i]][1] for i in range(len(sequences)) if nextPosition[i] > lastPosition[i])
    timePenalty = standardDeviation(timestamps) + (len(sequences) - len(timestamps)) * noMatchTimePenalty
    return timePenalty + eventDist

def initializeDirections(dimensions):
    allDirections = []
    for d in range(dimensions):
        dir = list(0 for _ in range(d)) + list(1 for _ in range(d, dimensions))
        allDirections += set(permutations(dir))
    return allDirections

def neighbours(currentPosition):
    global sequences
    global allDirections

    neighbours = []
    for d in allDirections:
        outOfBounds = False
        for i in range(len(d)):
            outOfBounds = outOfBounds or (currentPosition[i] + d[i] >= len(sequences[i]))
        if not outOfBounds:
            neighbours.append(list(sum(x) for x in zip(currentPosition, d)))
    return neighbours

def aStarTimeWarpingPathWithTimestamps(eventSequence):
    # initialize global variables
    global allDirections
    global sequences
    allDirections = initializeDirections(len(eventSequence))
    sequences = eventSequence

    # Dijkstra
    predecessors = {}
    nextPosition = []

    start = list(0 for _ in range(len(sequences)))
    stop = list(len(s) - 1 for s in sequences)

    # this will not impact the path, just the end cost
    startTimestamps = list(s[0][1] for s in sequences)
    startDist = standardDeviation(startTimestamps) + charDistWithTime(start)
    currentPosition = (0, start, startDist, start) # dist with heuristic, position, actualDist, predecessor
    heapq.heappush(nextPosition, currentPosition)

    while currentPosition[1] != stop:
        currentPosition = heapq.heappop(nextPosition)
        if tuple(currentPosition[1]) in predecessors:
            continue
        predecessors[tuple(currentPosition[1])] = currentPosition[3]
        for n in neighbours(currentPosition[1]):
            if tuple(n) not in predecessors:
                nDist = currentPosition[2] + withTimeDist(currentPosition[1], n, 0)
                heapq.heappush(nextPosition, (nDist + distHeuristic(n), n, nDist, currentPosition[1]))
    
    path = []
    pathPosition = currentPosition[1]
    path.append(pathPosition)
    while pathPosition != start:
        pathPosition = predecessors[tuple(pathPosition)]
        path.append(pathPosition)
    
    return reversed(path)

def timeWarpingPath(localSequences):
    # initialize global variables
    global allDirections
    global sequences
    allDirections = initializeDirections(len(localSequences))
    sequences = localSequences

    # Dijkstra
    predecessors = {}
    nextPosition = []

    start = list(0 for _ in range(len(sequences)))
    stop = list(len(s) - 1 for s in sequences)

    currentPosition = (charDist(start), start, start) # dist, position, predecessor
    heapq.heappush(nextPosition, currentPosition)

    while currentPosition[1] != stop:
        currentPosition = heapq.heappop(nextPosition)
        if tuple(currentPosition[1]) in predecessors:
            continue
        predecessors[tuple(currentPosition[1])] = currentPosition[2]
        for n in neighbours(currentPosition[1]):
            nDist = currentPosition[0] + spaceDist(currentPosition[1], n)
            heapq.heappush(nextPosition, (nDist, n, currentPosition[1]))
    
    path = []
    pathPosition = currentPosition[1]
    path.append(pathPosition)
    while pathPosition != start:
        pathPosition = predecessors[tuple(pathPosition)]
        path.append(pathPosition)
    
    return reversed(path)

def timeWarpingPathAStar(localSequences):
    # initialize global variables
    global allDirections
    global sequences
    allDirections = initializeDirections(len(localSequences))
    sequences = localSequences

    # A*
    predecessors = {}
    nextPosition = []

    start = list(0 for _ in range(len(sequences)))
    stop = list(len(s) - 1 for s in sequences)

    currentPosition = (0, start, charDist(start), start) # dist with heuristic, position, actualDist, predecessor
    heapq.heappush(nextPosition, currentPosition)

    while currentPosition[1] != stop:
        currentPosition = heapq.heappop(nextPosition)
        if tuple(currentPosition[1]) in predecessors:
            continue
        predecessors[tuple(currentPosition[1])] = currentPosition[3]
        for n in neighbours(currentPosition[1]):
            if tuple(n) not in predecessors:
                nDist = currentPosition[2] + spaceDist(currentPosition[1], n)
                heapq.heappush(nextPosition, (nDist + distHeuristic(n), n, nDist, currentPosition[1]))
    
    path = []
    pathPosition = currentPosition[1]
    path.append(pathPosition)
    while pathPosition != start:
        pathPosition = predecessors[tuple(pathPosition)]
        path.append(pathPosition)
    
    return reversed(path)

def sequenceRating(finalSequence, userSequence):
    path = timeWarpingPathAStar([finalSequence, userSequence])
    cost = 0
    lastPosition = [-1, -1]
    for position in path:
        if position[0] == lastPosition[0] or position[1] == lastPosition[1]:
            cost += 1
        elif userSequence[position[1]] == '*':
            cost += 0.5
        elif finalSequence[position[0]] != userSequence[position[1]]:
            cost += 1
        lastPosition = position
    # normalize errors 
    rating = float(cost) / float(len(finalSequence))
    return rating

def sequenceRatingWithTime(finalSequence, userSequence):
    path = aStarTimeWarpingPathWithTimestamps([finalSequence, userSequence])
    cost = 0
    lastPosition = [-1, -1]
    for position in path:
        # event type cost
        if position[0] == lastPosition[0] or position[1] == lastPosition[1]:
            cost += 1
        else:
            if userSequence[position[1]][0] == '*':
                cost += 0.5
            elif finalSequence[position[0]][0] != userSequence[position[1]][0]:
                cost += 1
            # this means that 1 sec differnece in time is equally as bad as having the wrong event type
            timeCost = 0.5 * (abs(finalSequence[position[0]][1] - userSequence[position[1]][1]).total_seconds())
            cost += timeCost
        lastPosition = position
    # normalize errors 
    rating = float(cost) / float(len(finalSequence))
    return rating