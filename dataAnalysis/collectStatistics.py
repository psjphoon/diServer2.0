# Python 2.7
import random
import string
import time

import costMatrixDijkstra as dij
import sequenceUtils as su
import timeSequenceUtils as tsu

def collectStatistics(wordLength, repetitions, wordNumber, errorProb):
    filename = "longStrings2.txt"
    file = open(filename, "a+")
    for rep in range(repetitions):
        originalSequence = su.randomword(wordLength)
        sequences = []
        for _ in range(wordNumber):
            newSequence = su.insertErrors(errorProb, originalSequence)
            sequences.append(newSequence)
        print(str(rep) + ": " + str(wordNumber) + " users, stringlength: " + str(wordLength) + ", errorProbability:" + str(errorProb) + "\n")

        before = time.time()
        path = dij.timeWarpingPathAStar(sequences)
        after = time.time()
        duration = after - before
        result = su.extractOriginal(path, sequences)
        rating = dij.sequenceRating(originalSequence, result)
        file.write(str(wordNumber) + "," + str(wordLength) + "," + str(errorProb) + "," + originalSequence + "," + result + "," + str(duration) + "," +str(rating) + "\n")
        
        print(originalSequence + "," + result + "," + str(duration) + "  " + str(rating) + "," + "\n")
    file.close()

def main():
    reps = 10
    errorProbs = [0.1]
    wordLengths = list(50 + i for i in range(700, 1000, 50))
    userNumbers = [3]
    for users in userNumbers:
        for errorProb in errorProbs:
            for wl in wordLengths:
                collectStatistics(wl, reps, users, errorProb)
    return

if __name__ == '__main__':
  main()
