import os
import random
import time

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
                    time.sleep(0.5)
                    print("Elevator's current floor is : {0}".format(self.currentFloor))
                    self.currentFloor +=1
            elif self.currentFloor > Destination:
                self.direction = 'down'
                self.sortFloorList()
                while self.currentFloor > Destination:
                    time.sleep(0.5)
                    print("Elevator's current floor is : {0}".format(self.currentFloor))
                    self.currentFloor -=1
            self.status = 'stopped'
            self.floorRequestList.pop(0)
        self.status = 'idle'
        time.sleep(0.5)
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
        time.sleep(0.5)
        print("Elevator's doors are opening")
        time.sleep(0.5)
        print("Waiting 5 seconds")
        self.door.status = 'closed'
        time.sleep(0.5)
        print()
        input("Press Enter to continue...")
        print()

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
        print("The best Elevator for you has the ID #{0} and is on the floor #{1}".format(elevator.ID, elevator.currentFloor))
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



### This bottom section is dedicated to pre-made and custom scenarios after running Pytest ###
## Toggle the comments from 188 to 270 to proceed ##

# #Creates the selected scenario
# def inputInputsInColumn(numberOfFloors, numberOfElevators, customScenario):

#     #Scenario selected by USER
#     userFloor = random.randrange(1, numberOfFloors)
#     possibleDirections = ['up', 'down']
#     userDirection = 'none'
#     userRequestedFloor = 0
#     elevatorsPossibleStatus = ['idle', 'moving']
#     print()
#     print("Scenario {0}".format(customScenario))
#     print()
#     print("This Column has {0} floors and {1} elevators".format(numberOfFloors,numberOfElevators))
#     column = Column(1, numberOfFloors, numberOfElevators)

#     for x in range(numberOfElevators):
#         random0to1 =  random.randrange(0,2)
#         column.elevatorList[x].currentFloor = random.randrange(1, numberOfFloors)
#         column.elevatorList[x].status = elevatorsPossibleStatus[random0to1]

#         if column.elevatorList[x].status == elevatorsPossibleStatus[1] and column.elevatorList[x].currentFloor == numberOfFloors:
#             column.elevatorList[x].direction = possibleDirections[1]
#         elif column.elevatorList[x].status == elevatorsPossibleStatus[1] and column.elevatorList[x].currentFloor == 1:
#             column.elevatorList[x].direction = possibleDirections[0]
#         else:
#             column.elevatorList[x].direction = possibleDirections[random.randrange(0,1)]
#             if column.elevatorList[x].direction == possibleDirections[0]:
#                 column.elevatorList[x].floorRequestList.append(random.randrange(column.elevatorList[x].currentFloor, numberOfFloors))
#             else:
#                 column.elevatorList[x].floorRequestList.append(random.randrange(1, column.elevatorList[x].currentFloor))
#         if column.elevatorList[x].status == elevatorsPossibleStatus[0]:
#             print("Elevator with ID #{0} is located at the floor #{1} and is {2}".format(column.elevatorList[x].ID,column.elevatorList[x].currentFloor, column.elevatorList[x].status))
#         else:
#             print("Elevator with ID #{0} is located at the floor #{1} and is {2} towards floor #{3}".format(column.elevatorList[x].ID,column.elevatorList[x].currentFloor, column.elevatorList[x].status, column.elevatorList[x].floorRequestList[0]))
#     print()
#     input("Press Enter to continue...")
#     print()

#     if userFloor == 1:
#         userDirection = possibleDirections[0]
#     elif userFloor == numberOfFloors:
#         userDirection = possibleDirections[1]
#     else:
#         userDirection = possibleDirections[random.randrange(0,1)]

#     if userDirection == possibleDirections[0] and userFloor == numberOfFloors - 1:
#         userRequestedFloor = numberOfFloors
#     elif userDirection == possibleDirections[1] and userFloor == 2:
#         userRequestedFloor = 1
#     elif userDirection == possibleDirections[0]:
#         userRequestedFloor = random.randrange(userFloor + 1, numberOfFloors)
#     else:
#         userRequestedFloor = random.randrange(1, userFloor - 1)
            
#     goodElevator = column.requestElevator(userFloor, userDirection)
#     print()
#     input("Press Enter to continue...")
#     print()
#     goodElevator.requestFloor(userRequestedFloor)

# #Scenario picker
# rightChoice = False

# print("Hello mister") 

# while rightChoice == False:
#     userScenarioChoice = input("Would you like to try the scenario {1}, {2}, {3} or {4} (#4 is customizable) ? : ")
#     if userScenarioChoice == '1':
#         inputInputsInColumn(10, 2, userScenarioChoice)
#         rightChoice = True
#     elif userScenarioChoice == '2':
#         inputInputsInColumn(15, 5, userScenarioChoice)
#         rightChoice = True
#     elif userScenarioChoice == '3':
#         inputInputsInColumn(30, 10, userScenarioChoice)
#     elif userScenarioChoice == '4':
#         userAmountOfFloors = int(input("How many floors do you want ? : "))
#         userAmountOfElevators = int(input("How many elevators do you want ? : "))
#         inputInputsInColumn(userAmountOfFloors, userAmountOfElevators, userScenarioChoice)
#         rightChoice = True
#     else:
#         os.system('cls')

# print("Thank you come again!")