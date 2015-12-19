from __future__ import print_function

import unittest
import sys
import os
import time

import numpy as np
import theano
import theano.tensor as T

import lasagne
from Dataset import Dataset

import trainWithLasagne as Network
import GridWorld
from Images import Images


class User(object):
    def loadNetworkState(self, fileName):
        print("Loading network from", fileName, "...")
        with np.load(fileName) as f:
            param_values = [f['arr_%d' % i] for i in range(len(f.files))]
            lasagne.layers.set_all_param_values(self.network, param_values)
        print("Done loading network from", fileName)
        return self

    def createNetwork(self, model='custom_mlp:2,800,0,0.3'):
        # model='mlp'
        # model='custom_mlp:2,800,0,0'
        # model='custom_mlp:8,400,0,0'
        # model='cnn10'

        # Prepare Theano variables for inputs and targets
        input_var = T.tensor4('inputs')

        # Create neural network model (depending on first command line parameter)
        print("Building model and compiling functions...")
        if model == 'mlp':
            network = Network.build_mlp(input_var)
        elif model.startswith('custom_mlp:'):
            depth, width, drop_in, drop_hid = model.split(':', 1)[1].split(',')
            network = Network.build_custom_mlp(input_var, int(depth), int(width),
                                       float(drop_in), float(drop_hid))
        elif model == 'cnn':
            network = Network.build_cnn(input_var)
        elif model == 'cnn10':
            network = Network.build_cnn10(input_var)
        else:
            print("Unrecognized model type %r." % model)
            return

        self.network = network
        self.input_var = input_var

        self.test_prediction = lasagne.layers.get_output(network, deterministic=True)
        self.predict_function = theano.function([input_var], self.test_prediction)
        # self.test = theano.function([input_var], self.test_prediction)

    def predictSample(self, sample):
        """Returns the list of actions, sorted by confidence.
        For example: preferedActions ['rightTop', 'right', 'top',
        'leftTop', 'rightBottom', 'unknown', 'left', 'leftBottom',
        'bottom', 'unknown']"""
        # test_data = theano.shared(np.asarray(test_data, dtype=theano.config.floatX))
        # test_data = theano.shared(sample)
        # test_data = theano.shared(np.asarray(sample))
        # test_data = theano.shared(np.asarray([x/101 for x in range(0, 100)]))
        # test_data = theano.shared(np.asarray(sample, dtype=theano.config.floatX))
        # test_data = sample


        test_data = sample[:].reshape(1, *sample.shape)
        preds = self.predict_function(test_data)
        # preds = np.array([[ 0.06705791,  0.25411619,  0.25517201,  0.15116946,  0.07407319,  0.06302036,   0.03683196,  0.02889933,  0.06965961]])
        # print("prediction:", preds)

        # print("direction:", GridWorld.Direction(np.argmax(preds)).name)
        preds = preds[0]

        preferedActions = []
        prob = 1
        while prob > 0:
            maxValuePosition = np.argmax(preds)
            prob = preds[maxValuePosition]
            preferedActions.append(GridWorld.Direction(maxValuePosition))
            preds[maxValuePosition] = 0
        # print("preferedActions", [direction.name for direction in preferedActions])
        return preferedActions

    def getNextPosition(self, world, start, direction):
        """Performs a move in the given direction, and return the destination
        cell. Returns None if the direction leads outside the world or in
        an obstacle."""
        col = start.col + direction.col()
        line = start.line + direction.line()
        if world.exists(col, line):
            destination = world.get(col, line)
            if destination.reachable:
                return destination
        return None

    def play(self, world, start, goal, verbose=False):
        found = False
        blocked = False
        stepsCount = 0
        records = []
        while not found and not blocked and stepsCount < 30:
            if start.col == goal.col and start.line == goal.line:  # if the goal has been reached
                found = True
                if verbose:
                    print("Step", stepsCount, ": Reached the goal in", start)
            else:
                stepsCount += 1
                sample = Dataset.gridWorldToGreyScaleSample(world, start, goal)
                actions = self.predictSample(sample)
                chosenAction = None
                for direction in actions:
                    nextPosition = self.getNextPosition(world, start, direction)
                    if nextPosition is not None:
                        chosenAction = direction
                        break
                if (nextPosition is None) or \
                   (start.col == nextPosition.col and start.line == nextPosition.line):    # if there is not any valid next position, or if next position is the same as current position
                    blocked = True
                    if verbose:
                        print("Step", stepsCount, ": Blocked in", start)
                if verbose:
                    print("Step", stepsCount, ": From", start, "move", chosenAction.name, "to", nextPosition, "(goal is in ", goal, ")")
                records.append((start, chosenAction, nextPosition))
                start = nextPosition
        return found, blocked, records

    def saveRecordsToFiles(self, world, start, goal, found, blocked, records, prefix="play_"):
        # for stepCount, (position, action, nextPosition) in enumerate(records):
        #     img = Images.worldToImage(world, position, goal)
        #     img.save(prefix + 'step' + str(stepCount).zfill(3) + '_willGo_' + action.name + '.png')
        if found:  # generate a last image with the player reaching the goal
            img = Images.worldToImage(world, goal, None)
            img.save(prefix + 'step' + str(len(records)).zfill(3) + '_success.png')



    def makeSample(self, world, start, goal):
        pass


class Tests(unittest.TestCase):
    db = Dataset.loadFrom('medium20000_10_shuffled_0.3obstacles.pkl')

    def setUp(self):
        pass

    def test_1(self):
        user = User()
        user.createNetwork(model='custom_mlp:2,800,0,0.3')
        user.loadNetworkState("model_customMlp2_800_0_0.3__10by10___30percentsAccuracy.npz")

        saveDir = "games"
        # for i in [0, 1, 2]: #range(Tests.db.X_test):
        for i in range(Tests.db.X_test.shape[0]):
            sample = Tests.db.X_test[i]
            world, start, goal = Dataset.greyScaleSampleToGridWorld(sample)
            found, blocked, records = user.play(world, start, goal)
            gameName = ""
            if found:
                gameName += "success"
            elif blocked:
                gameName += "blocked"
            else:
                gameName += "timeout"
            gameName += "_" + str(i).zfill(6)
            finalDir = saveDir + "/" + gameName + "/"
            # os.makedirs(finalDir)
            user.saveRecordsToFiles(world, start, goal, found, blocked, records, finalDir + gameName)

        # for i in range(Tests.db.X_train.shape[0]):
        #     user.predictSample(Tests.db.X_train[i])


        # world, start, goal = Dataset.greyScaleSampleToGridWorld(Tests.db.X_train[10])
        # user.predictSample(user.makeSample(world, start, goal))
        # user.predictSample(Tests.db.X_train[0])
        # user.predictSample(Tests.db.X_train[1])
        # user.predictSample(Tests.db.X_train[2])
        # user.predictSample(Tests.db.X_train[3])
        # user.predictSample(Tests.db.X_train[:2])
        # found, blocked, records = user.play(world, start, goal)
        # user.saveRecordsToFiles(world, start, goal, found, blocked, records, "games/test1/")
        pass


def dev():

    pass


if __name__ == '__main__':
    unittest.main()
    # dev()
