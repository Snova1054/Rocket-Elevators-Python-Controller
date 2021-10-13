import os
import random
import time
#RUN TEST WITH : python -m pytest (-v)
[elevatorID, floorRequestButtonID, callButtonID] = [1,1,1]

#Defines a Door
class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'off'

#Defines a Call Button
class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = 'off'
        self.floor = _floor
        self.direction = _direction

#Defines a Floor Request Button
class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = 'off'
        self.floor = _floor

#Defines an Elevator
class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'off'
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = 1
        self.direction = 'idle'
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []

        self.createFloorRequestButtons(self.amountOfFloors)
    #Creates a Floor request Button in each Elevator according to the number of Floors
    def createFloorRequestButtons(self, amountOfFloors):
        global floorRequestButtonID
        buttonFloor = 1
        for x in range(amountOfFloors):
            floorRequestButton = FloorRequestButton(floorRequestButtonID, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor +=1
            floorRequestButtonID +=1

    def requestFloor(self, Floor):
        print("New requested floor is : {0}".format(Floor))
        self.floorRequestList.append(Floor)
        self.move()
        self.operateDoors()

    #Moves the Elevator to the requested Floor
    def move(self):
        while len(self.floorRequestList) != 0:
            Destination = self.floorRequestList[0]
            self.status = 'moving'
            if self.currentFloor < Destination:
                self.direction = 'up'
                self.sortFloorList()
                while self.currentFloor < Destination:
                    time.sleep(1)
                    print("Elevator's current floor is : {0}".format(self.currentFloor))
                    self.currentFloor +=1
            elif self.currentFloor > Destination:
                self.direction = 'down'
                self.sortFloorList()
                while self.currentFloor > Destination:
                    time.sleep(1)
                    print("Elevator's current floor is : {0}".format(self.currentFloor))
                    self.currentFloor -=1
            self.status = 'stopped'
            self.floorRequestList.pop(0)
        self.status = 'idle'
        time.sleep(1)
        print("Elevator's arrived at the floor #{0}".format(self.currentFloor))
                
    #Sorts the floor requests List according to the Direction of the Elevator
    def sortFloorList(self):
        if self.direction == 'up':
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)

    #Opens and Closes the Doors of the Elevator
    def operateDoors(self):
        self.door.status = 'opened'
        time.sleep(1)
        print("Elevator's doors are opening")
        time.sleep(1)
        print("Waiting 5 seconds")
        self.door.status = 'closed'
        time.sleep(1)
        print("Elevator's doors are closing")

#Defines a Column
class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'idle'
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []

        self.createElevators(self.amountOfFloors, self.amountOfElevators)
        self.createCallButtons(self.amountOfFloors)
    
    #Creates call Button according to the number of Floors
    def createCallButtons(self, amountOfFloors):
        global callButtonID
        buttonFloor = 1

        for x in range(amountOfFloors):
            if buttonFloor < amountOfFloors:
                callButton = CallButton(callButtonID, buttonFloor, 'up')
                self.callButtonList.append(callButton)
                callButtonID +=1
            if buttonFloor>1:
                callButton = CallButton(callButtonID, buttonFloor, 'down')
                self.callButtonList.append(callButton)
                callButtonID +=1
            
            buttonFloor +=1
    
    #Creates Elevators according to the number of Floors and the number of Elevators
    def createElevators(self, amountOfFloors, amountOfElevators):
        global elevatorID
        for x in range(amountOfElevators):
            elevator = Elevator(elevatorID, amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID += 1
    
    #Requests an Elevator according a Floor and a Direction choosing the best Elevator
    def requestElevator(self, Floor, Direction):
        print("Requesting an Elevator for the floor #{0} to go {1}".format(Floor, Direction))
        elevator = self.findElevator(Floor, Direction)
        print("The best Elevator for you has the ID #{0}".format(elevator.ID))
        elevator.floorRequestList.append(Floor)
        elevator.move()
        elevator.operateDoors()
        return elevator
    
    #Finds the best Elevator according to the requested Floor and Direction
    def findElevator(self, requestFloor, requestedDirection):
        bestElevator = self.elevatorList[0]
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = type('bestElevatorInformations', (object,), {'bestElevator' : bestElevator, 'bestScore' : bestScore, 'referenceGap' : referenceGap})

        for x in range(len(self.elevatorList)):
            if requestFloor == self.elevatorList[x].currentFloor and self.elevatorList[x].status == 'stopped' and requestedDirection == self.elevatorList[x].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, self.elevatorList[x], bestScore, referenceGap, bestElevator, requestFloor)
            elif requestFloor > self.elevatorList[x].currentFloor and self.elevatorList[x].direction == 'up' and requestedDirection == self.elevatorList[x].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, self.elevatorList[x], bestScore, referenceGap, bestElevator, requestFloor)
            elif requestFloor < self.elevatorList[x].currentFloor and self.elevatorList[x].direction == 'down' and requestedDirection == self.elevatorList[x].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, self.elevatorList[x], bestScore, referenceGap, bestElevator, requestFloor)
            elif self.elevatorList[x].status == 'idle':
                bestElevatorInformations = self.checkIfElevatorIsBetter(3, self.elevatorList[x], bestScore, referenceGap, bestElevator, requestFloor)
            else:
                bestElevatorInformations = self.checkIfElevatorIsBetter(4, self.elevatorList[x], bestScore, referenceGap, bestElevator, requestFloor)
            bestElevator = bestElevatorInformations.bestElevator
            bestScore = bestElevatorInformations.bestScore
            referenceGap = bestElevatorInformations.referenceGap

        return bestElevatorInformations.bestElevator
    #Compares each Elevators to find the best
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, Floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - Floor)
        elif bestScore == scoreToCheck:
            Gap = abs(newElevator.currentFloor - Floor)
            if referenceGap > Gap:
                bestElevator = newElevator
                referenceGap = Gap
        bestElevatorInformations = type('bestElevatorInformations', (object,), {'bestElevator' : bestElevator, 'bestScore' : bestScore, 'referenceGap' : referenceGap})
        return bestElevatorInformations

#def printWithDelay(message):
    #time.sleep(1)
    #parint(message)
    
#Creates the selected scenario
def inputInputsInColumn(numberOfFloors, numberOfElevators, customScenario):

    #Scenario #1 selected by USER
    if customScenario == '1':
        print()
        print("Scenario 1")
        print()
        print("This Column has {0} floors and {1} elevators".format(numberOfFloors,numberOfElevators))
        column1 = Column(1, numberOfFloors, numberOfElevators)
        column1.elevatorList[0].currentFloor = 2
        column1.elevatorList[0].status = 'idle'
        column1.elevatorList[1].currentFloor = 6
        column1.elevatorList[1].status = 'idle'

        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[0].ID,column1.elevatorList[0].currentFloor, column1.elevatorList[0].status))
        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[1].ID,column1.elevatorList[1].currentFloor, column1.elevatorList[1].status))
        print()
        input("Are you ready?")
        print()
        goodElevator = column1.requestElevator(3, 'up')
        goodElevator.requestFloor(7)

    #Scenario #2 selected by USER
    elif customScenario == '2':
        print()
        print("Scenario 2")
        print()
        print("This Column has {0} floors and {1} elevators".format(numberOfFloors,numberOfElevators))
        column1 = Column(1, numberOfFloors, numberOfElevators)
        column1.elevatorList[0].currentFloor = 10
        column1.elevatorList[0].status = 'idle'
        column1.elevatorList[1].currentFloor = 3
        column1.elevatorList[1].status = 'idle'

        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[0].ID,column1.elevatorList[0].currentFloor, column1.elevatorList[0].status))
        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[1].ID,column1.elevatorList[1].currentFloor, column1.elevatorList[1].status))
        print()
        input("Are you ready?")
        print()
        goodElevator1 = column1.requestElevator(1, 'up')
        goodElevator1.requestFloor(6)

        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[0].ID,column1.elevatorList[0].currentFloor, column1.elevatorList[0].status))
        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[1].ID,column1.elevatorList[1].currentFloor, column1.elevatorList[1].status))
        goodElevator2 = column1.requestElevator(3, 'up')
        goodElevator2.requestFloor(5)

        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[0].ID,column1.elevatorList[0].currentFloor, column1.elevatorList[0].status))
        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[1].ID,column1.elevatorList[1].currentFloor, column1.elevatorList[1].status))
        goodElevator3 = column1.requestElevator(9, 'down')
        goodElevator3.requestFloor(2)

    #Scenario #3 selected by USER
    elif customScenario == '3':
        print()
        print("Scenario 3")
        print()
        print("This Column has {0} floors and {1} elevators".format(numberOfFloors,numberOfElevators))
        column1 = Column(1, numberOfFloors, numberOfElevators)
        column1.elevatorList[0].currentFloor = 10
        column1.elevatorList[0].status = 'idle'
        column1.elevatorList[1].currentFloor = 3
        column1.elevatorList[1].status = 'moving'
        column1.elevatorList[1].direction = 'up'
        column1.elevatorList[1].floorRequestList.append(6)


        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[0].ID,column1.elevatorList[0].currentFloor, column1.elevatorList[0].status))
        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[1].ID,column1.elevatorList[1].currentFloor, column1.elevatorList[1].status))
        print()
        input("Are you ready?")
        print()
        goodElevator1 = column1.requestElevator(1, 'up')
        goodElevator1.requestFloor(6)

        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[0].ID,column1.elevatorList[0].currentFloor, column1.elevatorList[0].status))
        print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[1].ID,column1.elevatorList[1].currentFloor, column1.elevatorList[1].status))
        goodElevator2 = column1.requestElevator(3, 'up')
        goodElevator2.requestFloor(5)

    #Customized scenario selected by USER
    elif customScenario == '0':
        print()
        print("Scenario 1")
        print()
        print("This Column has {0} floors and {1} elevators".format(numberOfFloors,numberOfElevators))
        print()
        input("Are you ready?")
        print()
        column1 = Column(1, numberOfFloors, numberOfElevators)
        for x in numberOfElevators:
            column1.elevatorList[x].currentFloor = random.randrange(1,numberOfFloors)
            print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column1.elevatorList[x].ID,column1.elevatorList[x].currentFloor, column1.elevatorList[x].status))
            column1.elevatorList[x].direction = 'idle'
            column1.elevatorList[x].status = 'idle'
            


userInputIsRight = False

while userInputIsRight == False:
    print("Hello mister") 
    userNumberInput = input("Would you like a predefined scenario {1} or a customized scenario {2} ? : ")
    if userNumberInput == '1':
        rightChoice = False
        while rightChoice == False:
            userScenarioChoice = input("Would you like to try the scenario {1}, {2} or {3} ? : ")
            if userScenarioChoice == '1' or userScenarioChoice == '2' or userScenarioChoice == '3':
                inputInputsInColumn(10, 2, userScenarioChoice)
                rightChoice = True
            else:
                os.system('cls')
        userInputIsRight = True
    elif userNumberInput == '2':
        inputInputsInColumn(10, 2, '0')
        userInputIsRight = True
    else:
        os.system('cls')
        userInputIsRight = False
    
print("Thank you come again!")