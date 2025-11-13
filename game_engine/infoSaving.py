class InfoSaving:
    textFileDirectory:str = ""
    
    def __init__(self) -> None:
        # Default initialisation for completeness
        self.textFileDirectory = ""

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

    # turn a text file with each record split by a line and the data split by commas into an array of Entry
    def readFile(self):
        entries:list[InfoSaving.Entry] = []

        fileWrapper = open(InfoSaving.textFileDirectory, "r")
        
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
            newEntry:InfoSaving.Entry = InfoSaving.Entry()

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
    def checkForExistingPlayer(entryList, name:str):
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

    def writeListToFile(entriesList:list[InfoSaving.Entry]):
        textFormat = ""
        with open(InfoSaving.textFileDirectory, "w") as textFile:
            for i in entriesList:
                textFormat = textFormat + i.name + ","
                textFormat = textFormat + str(i.wins) + ","
                textFormat = textFormat + str(i.losses) + "\n"

            textFormat = textFormat[0:len(textFormat) - 1]
            textFile.write(textFormat)

        textFile.close()
        
        
    def addScore(self, name:str, isWin:bool):
        entriesList = InfoSaving.readFile(InfoSaving.textFileDirectory)

        arrayPosition = InfoSaving.checkForExistingPlayer(entriesList, name) 

        if (arrayPosition == -1):
            newEntry:InfoSaving.Entry = InfoSaving.Entry()
            newEntry.name = name
            entriesList.append(newEntry)
            arrayPosition = len(entriesList) - 1

        if (isWin):
            entriesList[arrayPosition].wins = entriesList[arrayPosition].wins + 1
        else:
            entriesList[arrayPosition].losses = entriesList[arrayPosition].losses + 1
        
        InfoSaving.writeListToFile(entriesList)

#test:InfoSaving = InfoSaving()
#InfoSaving.textFileDirectory = "./game_engine/testfile.txt"
#test.textFileDirectory = "./game_engine/testfile.txt"

#test.addScore("a", True)
#test.addScore("b", False)
#test.addScore("c", True)
#test.addScore("c", True)
#test.addScore("c", False)
#test.addScore((chars + digits), True)