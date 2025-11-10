#
# Not fully finished yet
#

# each record will be an object of this class
class Entry(object):
    name:str
    wins:int
    losses:int

# turn a text file with each record split by a line and the data split by commas into an array of Entry
def readFile(textFile:str):
    entries = []

    textFile = open(textFile, "r")
    
    # get each line as an individual string in a list
    lines = textFile.read().split('\n')

    # initialise the array in which the individual data will be stored
    data = []
    
    # for every line of the text fine
    for i in lines:
        # split up the line using commas as the separation mark
        data.append(i.split(','))
    
    # initialise counter for getting the right column of data in the text file
    counter = 0

    # for each line
    for i in data:
        # create a new entry for a temporary store the information
        newEntry = Entry()

        # for each piece of data
        for j in i:
            # reset counter so that it does not go out of range of the array (> number is the amount of columns - 1)
            if (counter > len(i) - 1):
                counter = 0
        
            # check counter position for column
            if (counter == 0):
                newEntry.name = j
            elif counter == 1:
                newEntry.wins = int(j)
            else:
                newEntry.losses = int(j)
            # if any more columns are added then more elif statements need added
            
            counter = counter + 1
        
        # append new entry (row of data) to the list
        entries.append(newEntry)

    return entries

def main():
    # all entries will be stored in this list
    # process file into this array
    entryList = readFile("./server/testfile.txt") # currently a temporary file (not pushed to repository)

main()