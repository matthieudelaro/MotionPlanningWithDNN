import heapq
import unittest
from random import randint, shuffle
import math
from enum import Enum


class Direction(Enum):
    unknown = 0
    right = 1
    rightTop = 2
    top = 3
    leftTop = 4
    left = 5
    leftBottom = 6
    bottom = 7
    rightBottom = 8

    def col(self):
        if self.name in ["right", "rightBottom", "rightTop"]:
            return 1
        elif self.name in ["left", "leftBottom", "leftTop"]:
            return -1
        else:
            return 0

    def line(self):
        if self.name in ["top", "leftTop", "rightTop"]:
            return -1
        elif self.name in ["bottom", "rightBottom", "leftBottom"]:
            return 1
        else:
            return 0

    def cost(self):
        # return math.sqrt(self.col()**2 + self.line()**2)
        if self.value == 1:
            return 1.0
        if self.value == 2:
            return 1.4142135623730951
        if self.value == 3:
            return 1.0
        if self.value == 4:
            return 1.4142135623730951
        if self.value == 5:
            return 1.0
        if self.value == 6:
            return 1.4142135623730951
        if self.value == 7:
            return 1.0
        if self.value == 8:
            return 1.4142135623730951
        else:
            return 0
        # if self.name in ["right", "left", "top", "bottom"]:
        #     return 10
        # else:
        #     raise "Error"

    def fromTo(fromCell, toCell):
            # if fromCell.col == toCell.col and fromCell.line < toCell.line:
            #     return Direction.bottom
            # elif fromCell.col == toCell.col and fromCell.line > toCell.line:
            #     return Direction.top
            # elif fromCell.line == toCell.line and fromCell.col < toCell.col:
            #     return Direction.right
            # elif fromCell.line == toCell.line and fromCell.col > toCell.col:
            #     return Direction.left

            # # elif fromCell.col < toCell.col and fromCell.line < fromCell.line:
            # else:
            #     raise BaseException("from to error:" + str(fromCell) + " -> " + str(toCell))
            col = toCell.col - fromCell.col
            line = toCell.line - fromCell.line
            # for i in range(1, 9):
                # d = Direction(i)
            for d in Direction.directions():
                if d.col() == col and d.line() == line:
                    return d
            raise BaseException("from to error:" + str(fromCell) + " -> " + str(toCell))

    def directions():
        for i in range(1, 9):
            yield Direction(i)

    def __str__(self):
        if self.name == "right":
            return ">"
        elif self.name == "left":
            return "<"
        elif self.name == "top":
            return "^"
        elif self.name == "bottom":
            return "v"
        elif self.name == "leftTop":
            return "\\"
        elif self.name == "rightTop":
            return "/"
        elif self.name == "leftBottom":
            return ","
        elif self.name == "rightBottom":
            return "~"
        else:
            return "."


class Cell(object):
    def __init__(self, col, line, reachable):
        """Initialize new cell.
        @param reachable is cell reachable? not a wall?
        @param col cell col coordinate
        @param line cell line coordinate
        @param g cost to move from the starting cell to this cell.
        @param h estimation of the cost to move from this cell
                 to the ending cell.
        @param f f = g + h
        """
        self.reachable = reachable
        self.col = col
        self.line = line
        # self.parent = None
        # self.g = 0
        # self.h = 0
        # self.f = 0
        # self.solved = False

    def __lt__(self, other):
        return ("%s, %s" % (self.col, self.line) <
                "%s, %s" % (other.col, other.line))
        # return self.col < other.col and self.line < other.line

    def __str__(self):
        return "(%d, %d)" % (self.col, self.line)

    def __repr__(self):
        return "(%d, %d)" % (self.col, self.line)


class GridWorld(object):
    def __init__(self, width, height):
        # grid cells
        self.height = width
        self.width = height

        self.cells = [Cell(col, line, True)
                      for line in range(self.height)
                      for col in range(self.width)
                      ]

    def resetSearchData(self):
        for cell in self.cells:
            cell.parent = None
            cell.g = 0
            cell.h = 0
            cell.f = 0

    def resetSolveTags(self):
        for cell in self.cells:
            cell.solved = False

    def get(self, col, line):
        """Returns a cell from the cells list.
        @param col cell col coordinate
        @param line cell line coordinate
        @returns cell
        """
        # return self.cells[col * self.height + line]
        return self.cells[col + line * self.width]

    def exists(self, col, line):
        return (col >= 0 and col < self.width and
                line >= 0 and line < self.height)

    def set(self, col, line, cell):
        """Modifies a cell of the cells list.
        @param col cell col coordinate
        @param line cell line coordinate
        @returns cell
        """
        # return self.cells[col * self.height + line]
        self.cells[col + line * self.width] = cell
        return cell

    def getAdjacentCells(self, cell):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        # if cell.col < self.width-1:
        #     cells.append(self.get(cell.col+1, cell.line))
        # if cell.line > 0:
        #     cells.append(self.get(cell.col, cell.line-1))
        # if cell.col > 0:
        #     cells.append(self.get(cell.col-1, cell.line))
        # if cell.line < self.height-1:
        #     cells.append(self.get(cell.col, cell.line+1))
        for d in Direction.directions():
            col = cell.col + d.col()
            line = cell.line + d.line()
            if col >= 0 and line >= 0 and col < self.width and line < self.height:
                cells.append(self.get(col, line))

        return cells

    def getAccessibleCells(self, cell):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        for d in Direction.directions():
            col = cell.col + d.col()
            line = cell.line + d.line()
            if col >= 0 and line >= 0 and col < self.width and line < self.height:
                acc = self.get(col, line)
                if acc.reachable:
                    if self.get(cell.col, line).reachable or self.get(col, cell.line).reachable:  # make sure that at least one diagonal is reachable
                        cells.append(acc)

        return cells

    def addRandomObstacles(self, quantity):
        for _ in range(quantity):
            self._addRandomObstacle()

    def _addRandomObstacle(self):
        col = randint(0, self.width-1)
        line = randint(0, self.height-1)
        cell = self.get(col, line)
        if cell.reachable:
            cell.reachable = False
        else:
            cells = self.getAdjacentCells(cell)
            shuffle(cells)
            found = False
            for adj in cells:
                if adj.reachable:
                    adj.reachable = False
                    found = True
                    break
            if not found:
                self._addRandomObstacle()

    def __str__(self, separator=""):
        out = ""
        for i, cell in enumerate(self.cells):
            if (i % self.width) == 0:
                out += "\n"
            if cell.reachable:
                out += "." + separator
            else:
                out += "#" + separator
        return out

    def getLength(self):
        return self.height * self.width


    # def getCloseCells(self, cell):
    #     """Returns adjacent cells to a cell.
    #     Clockwise starting from the one on the right.
    #     @param cell get adjacent cells for this cell
    #     @returns adjacent cells list.
    #     """
    #     cells = self.getAdjacentCells(cell)
    #     if cell.col < self.width-1 && cell.line < self.height-1:
    #         cells.append(self.get(cell.col+1, cell.line+1))
    #     if cell.col < self.
    #     return cells


class Tests(unittest.TestCase):
    def setUp(self):
        self.world = GridWorld(10, 10)
        self.obstaclesProb = 0.2

    # def test_1(self):
    #     self.world.addRandomObstacles(math.floor(self.world.getLength() * self.obstaclesProb))
    #     print(self.world)
    #     pass

    # def test_2(self):
    #     adjs = self.world.getAdjacentCells(Cell(5, 5, True))
    #     for adj in adjs:
    #         adj.reachable = False
    #     print(adjs)
    #     print(self.world)

    # def test_3(self):
    #     self.world.get(5, 4).reachable = False
    #     self.world.get(6, 5).reachable = False
    #     adjs = self.world.getAccessibleCells(Cell(5, 5, True))
    #     for adj in adjs:
    #         adj.reachable = False
    #     print(adjs)
    #     print(self.world)

    def test_4(self):
        for d in Direction.directions():
            print("if self.value ==", d.value, ":")
            print("    return ", d.cost())

if __name__ == '__main__':
    unittest.main()
