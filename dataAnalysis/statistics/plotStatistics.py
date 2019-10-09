import itertools as it

import matplotlib.pyplot as plt


def dataFromFile(filename):
    file = open(filename, "r") 
    data = []
    lines = file.readlines()
    for line in lines:
        line = line.replace('\n', '')
        words = line.split(',')
        
        users = int(words[0])
        stringLength = int(words[1])
        errorProbability = float(words[2])
        # original = words[3]
        # result = words[4]
        time = float(words[5])
        score = float(words[6])
        
        data.append([users, stringLength, errorProbability, time, score])

    return data

def plot(xIndex, yIndex, aggregateIndex, data, xLabel = '', yLabel = '', aggregateLable = '', figureNumber = 0):
    if figureNumber > 0:
        plt.figure(figureNumber)
    distinctAggregateValues = set(line[aggregateIndex] for line in data)
    for dv in distinctAggregateValues:
        valuePairs = list((line[xIndex], line[yIndex]) for line in data if line[aggregateIndex] == dv)
        valuePairs.sort()
        xList = []
        yList = []
        for xValue, yPairs in it.groupby(valuePairs, lambda x: x[0]):
            xList.append(xValue)
            yValues = list(v[1] for v in yPairs)
            ySum = sum(yValues)
            yList.append(ySum/float(len(yValues)))

        line = plt.plot(xList, yList, label = str(dv))
        plt.legend(title=aggregateLable)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)

def main():
    filename = "data/moreThan3Reps.txt" 
    data = dataFromFile(filename)
    
    userNumberIndex = 0
    stringLengthIndex = 1
    errorProbabilityIndex = 2
    timeIndex = 3
    scoreIndex = 4

    plot(userNumberIndex, timeIndex, errorProbabilityIndex, data, "number of users", "time", "error probability", 1)
    plot(userNumberIndex, timeIndex, stringLengthIndex, data, "number of users", "time", "string length", 2)
    plot(stringLengthIndex, timeIndex, errorProbabilityIndex, data, "length of string", "time", "error probability", 3)
    plot(stringLengthIndex, timeIndex, userNumberIndex, data, "length of string", "time", "number of users", 4)
    plot(userNumberIndex, scoreIndex, errorProbabilityIndex, data, "number of users", "rating of result, normalized by string length", "error probability", 5)
    
    filename2 = "data/longStrings.txt"
    dataTwo = dataFromFile(filename2)
    plot(stringLengthIndex, timeIndex, errorProbabilityIndex, dataTwo, "length of string", "time", "error probability", 6)
    plt.show()    

if __name__ == '__main__':
  main()
