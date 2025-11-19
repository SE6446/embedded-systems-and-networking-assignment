class InfoSaving:
    textFileDirectory:str
    
    def __init__(self, textFile:str) -> None:
        # Default initialisation for completeness
        self.textFileDirectory = textFile

    

    # turn a text file with each record split by a line and the data split by commas into an array of Entry
    def readFile(self):
        entries:list[Entry] = []

        fileWrapper = open(self.textFileDirectory, "r")
        
        # get each line as an individual string in a list
        lines = fileWrapper.read().split('\n')

        fileWrapper.close() #Remember to close the file after reading!

        # initialise the array in which the individual data will be stored
        data: list[list[str]] = []
        
        # for every line of the text fine
        for i in lines:
            # split up the line using commas as the separation mark
            data.append(i.split(','))
        
        # initialise counter for getting the right column of data in the text file
        counter = 0

        # for each line
        for i in data:
            # create a new entry for a temporary store the information
            newEntry:Entry = Entry()

            # for each piece of data
            for j in i:
                # reset counter so that it does not go out of range of the array (> number is the amount of columns - 1)
                if (counter > len(i) - 1):
                    counter = 0
            
                # check counter position for column
                if (counter == 0):
                    newEntry.name = j
                elif counter == 1:
                    newEntry.wins = int(float(j))
                else:
                    newEntry.losses = int(float(j))
                # if any more columns are added then more elif statements need added
                
                counter = counter + 1
            
            # append new entry (row of data) to the list
            entries.append(newEntry)

        return entries

    # check to see if there is a record with a matching name already in the list, return the position if there is.  
    def checkForExistingPlayer(self, entryList, name:str):
        # to keep the position in the array
        counter:int = 0

        #for every entry
        for i in entryList:
            
            # go through every entry until a match is found
            if i.name == name:

                # return the position in the array
                return counter
            counter = counter + 1

        # -1 being returned means that there was not a matching record found in the array 
        return -1

    def writeListToFile(self, entriesList):
        textFormat = ""

        # open the text file that will be read into
        with open(self.textFileDirectory, "w") as textFile:

            # for every entry 
            for i in entriesList:
                # add the contents to one large string with extra for formatting
                textFormat = textFormat + i.name + ","
                textFormat = textFormat + str(i.wins) + ","
                textFormat = textFormat + str(i.losses) + "\n"

            # remove an extra \n that would break the function if it was left in
            textFormat = textFormat[0:len(textFormat) - 1]
            textFile.write(textFormat)

        textFile.close()
        
        
    def addScore(self, name:str, isWin:bool):

        # get the file in the form of an array
        entriesList = self.readFile()

        # find where in the array the desired player's record is, if it is not found, -1 is returned
        arrayPosition = self.checkForExistingPlayer(entriesList, name) 

        # add a new record with the new name
        if (arrayPosition == -1):
            newEntry:Entry = Entry()
            newEntry.name = name
            entriesList.append(newEntry)
            
            # amend array position so it is in line with the new record rather than -1
            arrayPosition = len(entriesList) - 1

        # add score
        if (isWin):
            entriesList[arrayPosition].wins = entriesList[arrayPosition].wins + 1
        else:
            entriesList[arrayPosition].losses = entriesList[arrayPosition].losses + 1
        
        self.writeListToFile(entriesList)

# copied over from server code
# each record will be an object of this class
class Entry:
    name:str
    wins:int
    losses:int
    def __init__(self) -> None:
        # Default initialisation for completeness
        self.name = ""
        self.wins = 0
        self.losses = 0

    def __str__(self) -> str:  # pyright: ignore[reportImplicitOverride]
        return f"Name: {self.name}, Wins: {self.wins}, Losses: {self.losses}"

#test:InfoSaving = InfoSaving()
#InfoSaving.textFileDirectory = "./game_engine/testfile.txt"
#test.textFileDirectory = "./game_engine/testfile.txt"

#test.addScore("a", True)
#test.addScore("b", False)
#test.addScore("c", True)
#test.addScore("c", True)
#test.addScore("c", False)
#test.addScore((chars + digits), True)
