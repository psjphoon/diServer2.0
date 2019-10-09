import math
import random
import re
import string
from collections import Counter


def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def insertErrors(errorProbability, sequence):
    i = 0
    while i < len(sequence):
        if random.uniform(0.0, 1.0) < errorProbability:
            change = random.choice(['delete', 'insert', 'replace'])
            if change == 'delete':
                sequence = sequence[:i] + sequence[i + 1:]
                i -= 1
            elif change == 'insert':
                sequence = sequence[:i] + random.choice(string.ascii_lowercase) + sequence[i:]
            elif change == 'replace':
                sequence = sequence[:i] + random.choice(string.ascii_lowercase) + sequence[i + 1:]  
        i += 1 
    return sequence         

def matchSequences(path, sequences):
    spacedSequences = []
    for _ in range(len(sequences)):
        spacedSequences.append('')
    lastPosition = list(-1 for _ in range(len(sequences)))
    for position in path:
        for i in range(len(position)):
            if position[i] != lastPosition[i]:
                spacedSequences[i] = spacedSequences[i] + sequences[i][position[i]]
            else:
                spacedSequences[i] = spacedSequences[i] + ' '
        lastPosition = position
    return spacedSequences

def extractOriginal(path, sequences):
    result = ''
    spacedSequences = matchSequences(path, sequences)
    index = 0
    while index < len(spacedSequences[0]):
        # decide on length on block
        stepLengths = []
        for s in spacedSequences:
            nextPosition = re.search(r'[^ ]', s[index:])
            steps = len(s[index:])
            if nextPosition != None:
                steps = nextPosition.span()[0]
            stepLengths.append(steps)
        blockLength = Counter(stepLengths).most_common()[0][0] + 1
        # decide on event
        events = ''
        
        # find most frequent entries in block
        for i in range(index, min(len(spacedSequences[0]), index + blockLength)):
            for sIndex in range(len(spacedSequences)):
                if spacedSequences[sIndex][i] != ' ':
                    events = events + spacedSequences[sIndex][i]
        occuranceNumbers = Counter(events).most_common()
        # no clear solution -> star
        if len(occuranceNumbers) > 1 and occuranceNumbers[0][1] == occuranceNumbers[1][1]:
            result = result + '*'
        else:
            result = result + occuranceNumbers[0][0]

        index += blockLength
    return result
