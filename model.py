import pandas as pd
class a_model:
    def __init__(self,start,goal, grid, state="searching", time=1000):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.state = state
        self.max_time = time
    

    def heuristic(self, a,b):
        #calculate the distance to place
        pass

    def get_neighbors(self,position):
        #findneighbors in grid - all travels possible
        if position not in self.grid:
            return []

        return self.grid[position]

    def find_path(self):
        #do algorithm return the path
        paths = []

        #list of paths
        paths = []
        
        #while not finished find new path
        # add path to paths

        #sort paths
        return paths