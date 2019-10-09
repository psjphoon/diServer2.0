from datetime import datetime
import collections

# an "enum" for informed access to the pressedButtons bitmap
class ButtonEnum:
    L1 = 0
    L2 = 1 
    Lup = 2
    Lright = 3
    Ldown = 4
    Lleft = 5
    Select = 6
    Start = 7
    R1 = 8
    R2 = 9
    Rgreen = 10
    Rred = 11
    Rblue = 12
    Rpink = 13
    numberOfButtons = 14

# creates a dictionary that points from the timestamp to the raw data collected at that time
def readEventFile(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    
    events = collections.OrderedDict()
    for line in lines:
        split = line.split(',')
        time = datetime.strptime(split[0], "%Y-%m-%d %H:%M:%S.%f")
        split.pop(0)
        events[time] = split
    return events

# creates a bitmap of which buttons are pressed according to the raw data
def dilongGamepadArrayToButtons(rawData):
    # default is no buttons are pressed
    # print (rawData)
    pressedButtons = [0,] * ButtonEnum.numberOfButtons

    # interpret every raw data entry
    # left horizontal
    rawValue = rawData[3]
    if int(rawValue) == 0:
        pressedButtons[ButtonEnum.Lleft] = 1
        # pBs.Lleft = 1
    elif int(rawValue) == 255:
        pressedButtons[ButtonEnum.Lright] = 1
        # pBs.Lright = 1
    
    # left vertical
    rawValue = rawData[4]
    if int(rawValue) == 0:
        # pBs.Lup = 1
        pressedButtons[ButtonEnum.Lup] = 1
    elif int(rawValue) == 255:
        # pBs.Ldown = 1
        pressedButtons[ButtonEnum.Ldown] = 1

    # right colored buttons
    rawValue = rawData[5]
    binary = str(bin(int(rawValue))[2:].zfill(8))

    pressedButtons[ButtonEnum.Rpink] = int(binary[0])
    pressedButtons[ButtonEnum.Rblue] = int(binary[1])
    pressedButtons[ButtonEnum.Rred] = int(binary[2])
    pressedButtons[ButtonEnum.Rgreen] = int(binary[3])

    # back buttons and select/start
    rawValue = rawData[6]
    binary = str(bin(int(rawValue))[2:].zfill(6))
    # print("binary of back buttons value:" + binary)
    pressedButtons[ButtonEnum.Start] = int(binary[0])
    pressedButtons[ButtonEnum.Select] = int(binary[1])
    pressedButtons[ButtonEnum.R1] = int(binary[2])
    pressedButtons[ButtonEnum.L1] = int(binary[3])
    pressedButtons[ButtonEnum.R2] = int(binary[4])
    pressedButtons[ButtonEnum.L2] = int(binary[5])
    # print(pressedButtons)
    return pressedButtons

def main():
    filename = "data/data_from_user_1"
    data = readEventFile(filename)
    #print(data)
    for key, value in data.iteritems():
        dilongGamepadArrayToButtons(value)

if __name__ == '__main__':
  main()
