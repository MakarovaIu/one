# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab
import abc

# from ps2_verify_movement37 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.7


class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.coordValidation(x, y)
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @staticmethod
    def coordValidation(x, y):
        try:
            float(x)
            float(y)
        except ValueError:
            print("x and y need to be numbers")

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.x, self.y
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    @staticmethod
    def roundPosition(pos):
        """ Returns the floor of x, the largest integer less than or equal to x """
        return Position(math.floor(pos.x), math.floor(pos.y))

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.checkWidthHeight(width, height)
        self._width = width
        self._height = height
        self.tiles = None
        self.tiles_state = None
        self.createTiles()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @staticmethod
    def checkWidthHeight(width, height):
        Position.coordValidation(width, height)
        if width < 0 or height < 0:
            raise ValueError("width and height need to be greater than 0")

    def createTiles(self):
        self.tiles = []
        for x in range(self.width):
            for y in range(self.height):
                self.tiles.append(Position(x, y))
        self.tiles_state = {(tile.x, tile.y): 'not cleaned' for tile in self.tiles}

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        pos = Position.roundPosition(pos)
        if self.isPositionInRoom(pos):
            self.tiles_state[(pos.x, pos.y)] = 'cleaned'
        else:
            raise ValueError("Position is not in the room")

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if type(m) is int and type(n) is int:
            return self.tiles_state[(m, n)] == 'cleaned'
        else:
            raise ValueError("Tile coordinates must be integers")
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return sum(state == 'cleaned' for state in self.tiles_state.values())

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return random.choice(self.tiles)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        if pos.x > self.width and pos.y > self.height:
            return False
        pos = Position.roundPosition(pos)
        return (pos.x, pos.y) in self.tiles_state.keys()


# === Problem 2
class Robot(metaclass=abc.ABCMeta):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.validateSpeed(speed)
        self._speed = float(speed)
        self.room = room
        self.position = self.room.getRandomPosition()
        self._direction = random.randrange(0, 360)
        self.room.cleanTileAtPosition(self.position)

    @property
    def speed(self):
        return self._speed
    
    @staticmethod
    def validateSpeed(speed):
        if speed < 0:
            raise ValueError("Speed should be equal or greater than 0")

    @property
    def position(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self._position

    @property
    def direction(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self._direction

    @position.setter
    def position(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self._position = position

    @direction.setter
    def direction(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self._direction = direction

    def helperUpdatePositionAndClean(self):
        new_position = self.position.getNewPosition(self.direction, self.speed)
        while not self.room.isPositionInRoom(new_position):
            self.direction = random.randrange(0, 360)
            new_position = self.position.getNewPosition(self.direction, self.speed)
        self.position = new_position
        self.room.cleanTileAtPosition(self.position)

    @abc.abstractmethod
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError  # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.helperUpdatePositionAndClean()


# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials, robot_type, animation=False):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """
    anim = None
    time_steps = []
    for _ in range(num_trials):
        if animation is True:
            anim = ps2_visualize.RobotVisualization(num_robots, width, height, 0.1)
        time_steps.append(runOneTrial(num_robots, speed, width, height, min_coverage, robot_type, anim))
    mean_time_steps = sum(time_steps)/len(time_steps)
    return mean_time_steps, anim


def runOneTrial(num_robots, speed, width, height, min_coverage, robot_type, anim=None):
    """The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT."""
    room = RectangularRoom(width, height)
    robots = [robot_type(room, speed) for _ in range(num_robots)]
    time_step = 0
    while min_coverage > room.getNumCleanedTiles()/room.getNumTiles():
        if anim is not None:
            anim.update(room, robots)
        for robot in robots:
            robot.updatePositionAndClean()
        time_step += 1
    return time_step


anim = None
# Uncomment this line to see how much your simulation takes on average
# res, anim = runSimulation(3, 1.0, 8, 8, 0.75, 3, StandardRobot, animation=True)
# print(res)


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.direction = random.randrange(0, 360)
        self.helperUpdatePositionAndClean()


# testRobotMovement(RandomWalkRobot, RectangularRoom)
# res, anim = runSimulation(3, 1.0, 8, 8, 0.75, 3, RandomWalkRobot, animation=True)
# print(res)
if anim is not None:
    anim.done()


def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()

    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 6
showPlot1("10 Robots To Clean 80% Of A Room", "Number of robots", "Time spent on cleaning")
showPlot2("Time It Takes Two Robots To Clean 80% Of Variously Shaped Rooms", "aspect ratio of the room", "Time spent on cleaning")
