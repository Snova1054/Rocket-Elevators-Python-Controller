#RUN TEST WITH : python -m pytest (-v)
[elevatorID, floorRequestButtonID, callButtonID] = [1,1,1]

#Defines a Column
class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'idle'
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []

        self.createElevators(self.amountOfFloors, self. amountOfElevators)
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
        print("Requesting an Elevator for the floor # : ", Floor, "to go ", Direction)
        elevator = self.findElevator(Floor, Direction)
        print("Best Elevator ID is : ", elevator.ID)
        elevator.floorRequestList.append(Floor)
        elevator.move()
        elevator.operateDoors()
        return elevator
    
    #Finds the best Elevator according to the requested Floor and Direction
    def findElevator(self, requestFloor, requestedDirection):
        bestElevator = self.elevatorList[0]
        bestScore = 5
        referenceGap = 10000000
        bestElevatorInformations = {bestElevator : bestElevator, bestScore : bestScore, referenceGap : referenceGap}

        for x in range(len(self.elevatorList)):
            if requestFloor == self.elevatorList[x].currentFloor and self.elevatorList[x].status == 'stopped' and requestedDirection == self.elevatorList[x].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, self.elevatorList[x], bestScore, referenceGap, bestElevator, requestFloor)
            elif requestFloor > self.elevatorList[x].currentFloor and self.elevatorList[x].status == 'up' and requestedDirection == self.elevatorList[x].direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, self.elevatorList[x], bestScore, referenceGap, bestElevator, requestFloor)
            elif requestFloor < self.elevatorList[x].currentFloor and self.elevatorList[x].status == 'down' and requestedDirection == self.elevatorList[x].direction:
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
        bestElevatorInformations = {bestElevator : bestElevator, bestScore : bestScore, referenceGap : referenceGap};
        return bestElevatorInformations

#Defines an Elevator
class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'off'
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = 1
        self.direction = 'idle'
        self.door = Door()
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
        print("New requested floor is : ", Floor)
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
                    print("Elevator's current floor is : ", self.currentFloor)
                    self.currentFloor +=1
            elif self.currentFloor > Destination:
                self.direction = 'down'
                self.sortFloorList()
                while self.currentFloor > Destination:
                    print("Elevator's current floor is : ", self.currentFloor)
            self.status = 'stopped'
            self.floorRequestList.pop(0)
        self.status = 'idle'
        print("Elevator's arrived at the floor # : ", self.currentFloor)
                
    #Sorts the floor requests List according to the Direction of the Elevator
    def sortFloorList(self):
        if self.direction == 'up':
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)

    #Opens and Closes the Doors of the Elevator
    def operateDoors(self):
        self.door.status = 'opened'
        print("Elevator's doors are opened")
        print("Waiting 5 seconds")
        self.door.status = 'closed'
        print("Elevator's doors are closed")

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

#Defines a Door
class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'off'