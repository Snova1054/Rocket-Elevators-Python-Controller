# Rocket-Elevators-Python-Controller
## Description

This controller's whole purpose is to handle a personalized amount of elevators with a personalized amount of floors in a single column.

It can be controlled first from the outside of an elevator on each floor and after that, from the inside a specific elevator.

When used called from outside, the column sends the best elevator possible from the user's current floor and direction. Then, when used from the inside of the elevator that was selected by the column, the elevator is moved to the to the user's destination.

Elevator selection is based on the elevator's status, current floor, direction and floor request list and on the user's floor and direction.

## Dependencies

### To be able to try the program with your own settings you only need to follow the instructions given by the console after running the program after the following:

- First you need to run the "residential_controller.py" in Visual Studio Code or Visual Studio:
- Then follow the instructions given by the console.

#### Each scenario:
##### Keep in mind that every elevator's current floor, status, direction and destination is randomnly generated. As is the user's current floor, direction and destination.
- Scenario 1 has `10` floors and `2` elevators
- Scenario 2 has `15` floors and `5` elevators
- Scenario 3 has `30` floors and `10` elevators
- Scenario 4 is special. You can input as many floors and elevators as you want.

```
bestElevator.requestFloor(floor)
```

### And now, to run the tests for this program you need Node JS and NPM installed and then you need to first run in your Terminal:
```
npm install
```

and then, to run the tests, input:

```
npm test
```