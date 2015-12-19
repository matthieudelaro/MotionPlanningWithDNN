import unittest
from AStar import AStar
from random import randint
import GridWorld
import math
import Flow
from Dataset import Dataset
import numpy as np


class Generator(object):
    def __init__(self, size):
        """Generated maps will be size*size maps."""
        self.size = size

    def generate(self, samplesQuantity, obstaclesProb=0.3, dataAugmentation=True):
        """Generate a list of given quantity of samples."""
        quantitySamplesGenerated = 0
        # samples = np.empty(shape=(samplesQuantity,), dtype=object)
        samples = np.empty(shape=(samplesQuantity, 1, self.size, self.size), dtype=float)
        labels = np.empty(shape=(samplesQuantity,), dtype="byte")
        # for _ in range(worldsQuantity):
        # while quantitySamplesGenerated < samplesQuantity:

        def getValidRandomGoal(world):
            while True:
                goal = world.cells[randint(0, len(world.cells)-1)]
                if goal.reachable:
                    return goal

        worldsQuantity = 0
        while True:
            # print("new world")
            # generate an area with obstacles
            world = GridWorld.GridWorld(self.size, self.size)
            obstaclesQuantity = math.floor(obstaclesProb * world.getLength())
            world.addRandomObstacles(obstaclesQuantity)

            if worldsQuantity == 0:
                print("Example of world:")
                print(world.__str__(" "))

            # for goal in world.cells:
            # with getValidRandomGoal(world) as goal:
            goal = getValidRandomGoal(world)
            worldsQuantity += 1
            if True:
                # if quantitySamplesGenerated >= samplesQuantity:
                    # break

                if goal.reachable:  # for each possible goal location
                    solution = Flow.solve(world, goal)  # solve the world
                    goalInSolution = solution.get(goal.col, goal.line)
                    print(Flow.enigmaAsStr(solution, goalInSolution, " "))
                    a = 0/0

                    for startCell in solution.cells:  # create a sample for each reachable cell
                        if startCell.reachable and startCell != goalInSolution:
                            for line in range(solution.height):
                                for col in range(solution.width):
                                    cell = solution.get(line, col)
                                    if cell == goalInSolution:
                                        # print("goal in solution", cell)
                                        samples[quantitySamplesGenerated, 0, col, line] = Dataset.GreyScales.goal
                                    elif cell == startCell:
                                        # print("start in solution", startCell)
                                        samples[quantitySamplesGenerated, 0, col, line] = Dataset.GreyScales.start
                                    elif cell.reachable:
                                        samples[quantitySamplesGenerated, 0, col, line] = Dataset.GreyScales.reachable
                                    else:
                                        samples[quantitySamplesGenerated, 0, col, line] = Dataset.GreyScales.obstacle
                            labels[quantitySamplesGenerated] = startCell.direction.value
                            # print("Added:", Flow.enigmaAsStr(solution, goalInSolution))
                            # print(samples[quantitySamplesGenerated, 0], " go ", Flow.Direction(labels[quantitySamplesGenerated]).name)
                            quantitySamplesGenerated += 1
                            if quantitySamplesGenerated == samplesQuantity:
                                return samples, labels
                            if quantitySamplesGenerated % math.ceil(samplesQuantity / 20) == 0:
                                print("\t Generating:", math.ceil((quantitySamplesGenerated/samplesQuantity)*100), "%. So far,", worldsQuantity, "worlds.")

    def shuffle_in_unison_scary(a, b):
        rng_state = np.random.get_state()
        np.random.shuffle(a)
        np.random.set_state(rng_state)
        np.random.shuffle(b)


class Tests(unittest.TestCase):
    def setUp(self):
        self.generator = Generator(3)
        pass

    def test_1(self):
        samples, labels = self.generator.generate(10)
        print("example\n", samples[1], Flow.Direction(labels[1]).name)
        pass


def dev():
    generator = Generator(10)
    print("Generating...")
    samples, labels = generator.generate(20000)
    print("Done generating. Shuffling...")
    Generator.shuffle_in_unison_scary(samples, labels)
    print("Done shuffling. Splitting...")
    db = Dataset()
    db.init(samples, labels, 17000, 1500)
    print("Done splitting. Saving...")
    fileName = 'medium20000_10_shuffled_0.3obstacles.pkl'
    db.saveTo(fileName)
    print("Done saving to", fileName)
    # print("Example of world:", db.X_train[0])


if __name__ == '__main__':
    # unittest.main()
    dev()
