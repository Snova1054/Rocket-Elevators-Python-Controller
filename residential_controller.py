[elevatorID, floorRequestButtonID, callButtonID] = [1,1,1]

class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'idle'
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []

class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'off'
        self._amountOfFloors = _amountOfFloors
        self.currentFloor = 1
        self.direction = 'idle'
        self.door = Door
        self.floorRequestButton = []
        self.floorRequestList = []


class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = 'off'
        self.floor = _floor
        self.direction = _direction

class FloorRequestButton:
    def __init__(self, _id, _floor):
        self.ID = _id
        self.status = 'off'
        self.floor = _floor

class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'off'