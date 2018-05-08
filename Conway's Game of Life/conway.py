import matplotlib.animation as anim
import matplotlib.pyplot as plt
import numpy as np

class Conway:
    def __init__(self, grid):
        self.grid = grid
        self.r = self.grid.rows
        self.c = self.grid.cols

        self.figure, self.axes = plt.subplots()
        self.cont = self.axes.matshow(self.getVal())
        self.last = self.getVal()

    def getVal(self):
        grid = [ [ self.grid.tiles[i][j].alive for j in range(self.c) ] for i in range(self.r) ]

        return grid

    def tick(self, guess):
        newGrid = [ [ 0 for j in range(self.c) ] for i in range(self.r) ]
        newGrid = self.getVal()
        #newGrid = self.last

        for i in range(self.r):
            for j in range(self.c):
                tile = self.grid.tiles[i][j]
                neighbors = tile.getNeighbors()
                print(neighbors)

                if tile.alive and (neighbors == 2 or neighbors == 3):
                    newGrid[i][j] = tile.alive

                elif tile.alive and (neighbors < 2 or neighbors > 3):
                    newGrid[i][j] = 0

                elif not tile.alive and neighbors == 3:
                    newGrid[i][j] = 1

        self.cont.set_data(newGrid)

        for i in range(self.grid.rows):
            for j in range(self.grid.cols):
                self.grid.tiles[i][j].grid = newGrid

        return self.cont

    def simulate(self, max_epoch=50):
        ani = anim.FuncAnimation(self.figure, self.tick, interval=500)
        plt.show()

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.tiles = self.initializeGrid()

    def initializeGrid(self):
        grid = [ [] for i in range(self.rows) ]

        for row in range(self.rows):
            for col in range(self.cols):
                alive = np.random.randint(0, 2)
                pos = (row, col)
                grid[row].append(Tile(self, pos, alive))

        return grid

    def setGrid(self, grid):
        for i in range(self.rows):
            for j in range(self.cols):
                alive = grid[i][j]
                pos = (i, j)
                self.tiles[i][j] = Tile(grid, pos, alive)

class Tile:
    def __init__(self, grid, pos, alive):
        self.grid = grid
        self.x, self.y = pos
        self.alive = alive

    def getNeighbors(self):
        neighbors = 0

        for i in range(self.x-1, self.x+2):
            for j in range(self.y-1, self.y+2):
                if i < 0 or j < 0 or i > self.grid.rows-1 or j > self.grid.cols-1:
                    continue

                if i == self.x and j == self.y:
                    continue

                if self.grid.tiles[i][j].alive:
                    neighbors += 1

        return neighbors

if __name__ == '__main__':
    np.random.seed(0)
    grid = Grid(4, 4)
    conway = Conway(grid)
    conway.simulate()

