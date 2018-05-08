import numpy as np
import tdl

class Conway:
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.grid = np.random.randint(0, 2, size=(m, n))
        self.root = tdl.init(m, n, title="Conway's Game of Life", fullscreen=False)


    def tick(self):
        newGrid = self.grid.copy()

        for i in range(self.m):
            for j in range(self.n):
                cell = newGrid[i][j]
                neighbors = self.getNeighbors(i, j, self.grid)

                if cell:
                    if neighbors < 2 or neighbors > 3:
                        newGrid[i, j] = 0

                else:
                    if neighbors == 3:
                        newGrid[i, j] = 1

        return newGrid
        self.grid = newGrid

    def getNeighbors(self, x, y, grid):
        neighbors = 0

        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i < 0 or j < 0:
                    continue

                if i > self.m-1 or j > self.n-1:
                    continue

                if i == x and j == y:
                    continue

                if grid[i][j]:
                    neighbors += 1

        return neighbors

    def simulate(self):
        while not tdl.event.is_window_closed():
            for i in range(self.m):
                for j in range(self.n):
                    if self.grid[i][j]:
                        self.root.draw_char(i, j, None, fg=None, bg=(255,0,0))

                    else:
                        self.root.draw_char(i, j, None, fg=None, bg=(0,0,255))

            tdl.flush()
            self.grid = self.tick()

np.random.seed(0)
conway = Conway(4, 4)
conway.simulate()
