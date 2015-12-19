from GridWorld import GridWorld, Direction
import math
import unittest


class Cell(object):
    def __init__(self, cell):
        self.direction = Direction.unknown
        self.cost = -1
        self.col = cell.col
        self.line = cell.line
        self.reachable = cell.reachable

    def __str__(self):
        return "(%d, %d)" % (self.col, self.line)

    def __repr__(self):
        return "(%d, %d)" % (self.col, self.line)


def solve(world, goalInWorld):
    solution = GridWorld(world.width, world.height)
    # print(solution.cells)
    solution.cells = [Cell(cell) for cell in world.cells]
    # print(solution.cells)
    goal = solution.get(goalInWorld.col, goalInWorld.line)
    goal.cost = 0
    closed = []
    opened = [goal]

    # reopen = 0

    while len(opened):
        # print(enigmaAsStr(solution, goal))
        # print("opened:", [(c.col, c.line) for c in opened])
        cell = opened.pop()
        closed.append(cell)

        # for adj in solution.getAdjacentCells(cell):
        for adj in solution.getAccessibleCells(cell):
            # print("cell", cell, "has got a adj", adj)
            if adj.reachable:  # we ignore obstacles
                direction = Direction.fromTo(adj, cell)
                cost = cell.cost + direction.cost()
                if adj.cost == -1:  # or adj.cost > cost:  # if not used yet
                    adj.direction = direction
                    adj.cost = cost
                    opened.append(adj)
                if adj.cost > cost:  # if not used yet
                    # reopen += 1
                    # print("reopen", reopen)
                    adj.direction = direction
                    adj.cost = cost
                    opened.append(adj)
    return solution


def enigmaAsStr(solution, goalInWorld, separator=""):
    goal = solution.get(goalInWorld.col, goalInWorld.line)
    out = ""
    for i, cell in enumerate(solution.cells):
        if (i % solution.width) == 0:
            out += "\n"
        if cell == goal:
            out += "E" + separator
        elif not cell.reachable:
            out += "#" + separator
        else:
            out += str(cell.direction) + separator
    return out


class Tests(unittest.TestCase):
    def setUp(self):
        self.world = GridWorld(10, 10)
        self.obstaclesProb = 0.2
        self.world.addRandomObstacles(math.floor(self.world.getLength() * self.obstaclesProb))
        for cell in self.world.cells:
            if cell.reachable:
                self.goal = cell
                break

    def test_runs(self):
        solution = solve(self.world, self.goal)
        print(enigmaAsStr(solution, self.goal))

if __name__ == '__main__':
    unittest.main()
    # print(dir(Direction))

