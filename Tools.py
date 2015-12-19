import math
import unittest
import numpy


def poisson(l, k):
    return math.exp(k*math.log(l) - l - math.lgamma(k+1))


def randPoisson(min, max):
    return min + numpy.random.poisson((max-min)/2)


def randPoissonMean(mean):
    return numpy.random.poisson(mean)


class Tests(unittest.TestCase):
    def setUp(self):
        self.x = [x for x in range(11)]
        # self.x = [x/10 for x in range(100)]

    def test_poisson(self):
        l = 5
        res = [poisson(l, k) for k in self.x]
        # print(res)

    def test_randPoisson(self):
        res = {}
        for x in range(100):
            v = randPoisson(10, 20)
            if (res.get(v) is None):
                res[v] = 1
            else:
                res[v] += 1
        print(res)

if __name__ == '__main__':
    unittest.main()
