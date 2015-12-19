import pickle
import GridWorld
import numpy as np


class Dataset:
    class GreyScales:
        obstacle = 0
        goal = 100 / 255
        start = 170 / 255
        reachable = 255 / 255

    def init(self, samples, labels, trainingQuantity, validationQuantity):
        # X_train, y_train, X_val, y_val, X_test, y_test
        shapeS = samples.shape
        self.X_train = samples[0:trainingQuantity]
        self.X_val = samples[trainingQuantity:trainingQuantity + validationQuantity]
        self.X_test = samples[trainingQuantity + validationQuantity:]
        self.y_train = labels[0:trainingQuantity]
        self.y_val = labels[trainingQuantity:trainingQuantity + validationQuantity]
        self.y_test = labels[trainingQuantity + validationQuantity:]

    def saveTo(self, path):
        f_write = open(path, 'bw')
        pickle.dump(self, f_write, protocol=4, fix_imports=False)
        f_write.close()

    def loadFrom(path):
        print("Loading dataset from file", path)
        f_read = open(path, 'br')
        data = pickle.load(f_read)
        f_read.close()
        print("Dataset loaded from file.")
        return data

    def greyScaleSampleToGridWorld(sample):
        """Returns (GridWorld, start cell, goal cell)"""
        whatever, width, height = sample.shape
        world = GridWorld.GridWorld(width, height)

        goal = None
        start = None

        for line in range(height):
            for col in range(width):
                value = sample[0, col, line]
                if value == Dataset.GreyScales.goal:
                    goal = world.set(col, line, GridWorld.Cell(col, line, True))
                elif value == Dataset.GreyScales.start:
                    start = world.set(col, line, GridWorld.Cell(col, line, True))
                elif value == Dataset.GreyScales.obstacle:
                    world.set(col, line, GridWorld.Cell(col, line, False))
                else:
                    world.set(col, line, GridWorld.Cell(col, line, True))

        return world, start, goal

    def gridWorldToGreyScaleSample(world, start, goal):
        sample = np.empty(shape=(1, world.width, world.height), dtype=float)
        for line in range(world.height):
            for col in range(world.width):
                cell = world.get(line, col)
                if cell == goal:
                    # print("goal in solution", cell)
                    sample[0, col, line] = Dataset.GreyScales.goal
                elif cell == start:
                    # print("start in solution", startCell)
                    sample[0, col, line] = Dataset.GreyScales.start
                elif cell.reachable:
                    sample[0, col, line] = Dataset.GreyScales.reachable
                else:
                    sample[0, col, line] = Dataset.GreyScales.obstacle
        return sample
