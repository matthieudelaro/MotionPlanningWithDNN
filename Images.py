from PIL import Image
import unittest
from Dataset import Dataset
# import GridWorld


class Images(object):
    class BasicColors:
        obstacle = (0, 0, 0)
        goal = (10, 200, 10)
        start = (200, 10, 10)
        reachable = (255, 255, 255)

    def worldToImage(world, start=None, goal=None, colors=BasicColors):
        if goal is not None:
            goal = world.get(goal.col, goal.line)
        if start is not None:
            start = world.get(start.col, start.line)

        out = []
        for i, cell in enumerate(world.cells):
            # if (i % world.width) == 0:
                # out += "\n"
            if cell == start:
                out.append(colors.start)
            elif cell == goal:
                out.append(colors.goal)
            elif not cell.reachable:
                out.append(colors.obstacle)
            else:
                out.append(colors.reachable)

        img = Image.new('RGB', (world.width, world.height))
        img.putdata(out)
        # img.show()
        return img

# img = Image.new('RGB', (width, height))
# img.putdata(my_list)
# img.save('image.png')


class Tests(unittest.TestCase):
    db = Dataset.loadFrom('medium20000_10_shuffled_0.5obstacles.pkl')

    def setUp(self):
        pass

    def test_1(self):
        world, start, goal = Dataset.greyScaleSampleToGridWorld(Tests.db.X_train[2])
        # print(world[0])
        img = Images.worldToImage(world, start, goal)
        pass


def dev():
    pass


if __name__ == '__main__':
    unittest.main()
    # dev()


