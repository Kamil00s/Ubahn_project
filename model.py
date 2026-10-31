import pandas as pd
import heapq
from geopy.distance import geodesic
from timer import timer

class a_model:
    
    def __init__(self, graph, time=2, v_max=80, p_max = 40):
        self.WALK_SPEED = 5
        self.MAX_WALK_TIME = 20 # maximum walking time in minutes
        self.graph = graph
        self.status = "idle"
        self.max_time = time
        self.v_max = v_max
        self.coords = {}
        self.run_time = 0.0
        self.best_cost = 0.0
        self.p_max = p_max
        for s, travels in self.graph.items():
            for t in travels:
                self.coords[s] = (t["from_lat"], t["from_lon"])
                self.coords[t["to"]] = (t["to_lat"],t["to_lon"])
    

    def heuristic(self, a,b):
        # estimate the remaining travel time using straight-line distance and maximum speed
        dist = geodesic(a, b).meters / 1000
        cost = (dist / self.v_max) * 60
        return cost

    def get_neighbors(self,position):
        # find neighbors in graph - all travels possible
        if position not in self.graph:
            return []
        res = []
        for line in self.graph[position]:
            d = {
                "from": position,
                "to": line["to"],
                "cost_min": line["cost_min"],
                "action": line["action"],
            }
            res.append(d)
        return res
    
    def walking_distance_km(self,lat1,lon1,lat2,lon2):
        # find distance between two points
        dist = geodesic((lat1,lon1),(lat2,lon2)).meters / 1000
        return dist

    def walk_min(self,a,b):
        return self.walking_distance_km(a[0],a[1],b[0],b[1]) / self.WALK_SPEED * 60
    

    # calculate all the moves possible
    def get_moves(self,node,goal):

        # moves = tuples: (node_from, node_to, cost_min, action, heuristics)
        moves = []
        if node == "START":
            # allow direct walking only if it stays within the maximum walking time
            direct_walk_time = self.walk_min(self.coords[node], goal)
            if direct_walk_time <= self.MAX_WALK_TIME:
                moves.append((node, "GOAL", direct_walk_time, "walk", 0))
            # walk only to stations reachable within the maximum walking time
            for n in self.graph:
                station_walk_time = self.walk_min(self.coords[node], self.coords[n])
                if station_walk_time <= self.MAX_WALK_TIME:
                    moves.append((node, n, station_walk_time, "walk", self.heuristic(self.coords[n], goal)))
        # travel or transfer
        else:
            for d in self.get_neighbors(node):
                moves.append((node, d["to"], d["cost_min"], d["action"],
                              self.heuristic(self.coords[d["to"]], goal)))
            # walk from the station to the goal only within the maximum walking time
            goal_walk_time = self.walk_min(self.coords[node], goal)
            if goal_walk_time <= self.MAX_WALK_TIME:
                moves.append((node, "GOAL", goal_walk_time, "walk", 0))
        return moves

    @timer
    def find_path(self, start, goal):
        # node = station and line, additional signs are "START" and "GOAL"
        # move tuple = (node_from, node_to, cost_min, action, heuristics)
        # start, goal = (lat,lon) 

        # set the start and goal in coords dict
        self.coords["START"] = start 
        self.coords["GOAL"] = goal

        open_list = [(0, 0, "START", 0)]   # (f, g, node, path_length), smallest f wins
        best_g = {("START", 0): 0}         # cheapest known cost for each node and path length
        parent = {("START", 0): None}      # store the previous state and move for path reconstruction

        self.states_examined = 0            # count of states examined
        self.max_open_size = len(open_list) # track the maximum number of paths in the priority queue
        self.path_limit_reached = False     # flag to indicate if the path limit has been reached
        self.best_solution = None           # store the best solution found
        self.best_goal_state = None         # store the best goal state found

        while open_list and self.status == "searching":
            # we use heapq that outputs node with the lowest f
            f, g, node, length = heapq.heappop(open_list)
            # skip if a cheaper path to this node and length has already been found
            if g > best_g[(node, length)]:
                continue         
            self.states_examined += 1       # count each valid state examined by A*

            # algorithm found goal -> reverse and return the path
            if node == "GOAL":
                result = []
                state = (node, length)      # start reconstructing the path from the goal state
                # follow the parent pointers back to the start
                while parent[state] is not None:
                    state, move = parent[state]
                    result.append(move)
                result.reverse()                                    # reverse the path to get it from start to goal
                self.best_cost = sum(cost[2] for cost in result)    # calculate the total cost of the path
                self.best_solution = result                         # store the best solution found
                # warn if the solution reaches p_max and other paths were blocked
                if length == self.p_max and self.path_limit_reached:
                    print("potenziell nicht optimale Lösung gefunden")
                return result

            # try all moves from this node if its not goal
            for move in self.get_moves(node, goal):
                _, nxt, cost, _, h = move
                new_g = g + cost
                # increase the path length by 1 for each move
                new_length = length + 1
                # skip paths that exceed the maximum allowed length
                if new_length > self.p_max:
                    self.path_limit_reached = True
                    continue
                # keep the path if it is cheaper than any previously found path to the same node and length
                if new_g < best_g.get((nxt, new_length), float("inf")):
                    best_g[(nxt, new_length)] = new_g
                    # save the previous state and the move that led to this state for path reconstruction
                    parent[(nxt, new_length)] = ((node, length), move)
                    # check whether this valid path reaches the goal
                    if nxt == "GOAL" and (
                        self.best_goal_state is None
                        or new_g < best_g[self.best_goal_state]
                    ):
                        # save the cheapest goal state found so far
                        self.best_goal_state = (nxt, new_length)
                    # add the new path to the priority queue, including its length
                    heapq.heappush(open_list, (new_g + h, new_g, nxt, new_length))
                    # update the maximum size of the priority queue
                    self.max_open_size = max(
                        self.max_open_size,
                        len(open_list)
                        )
                    
        # report if no solution was found due to path length limit
        if self.status == "searching" and self.path_limit_reached and not open_list:
            print("Lösung mit begrenztem Speicher nicht generierbar")

        #return the best complete path found before the time limit
        if self.status == "stopped" and self.best_goal_state is not None:
            state = self.best_goal_state
            result = []

            while parent[state] is not None:
                state, move = parent[state]
                result.append(move)

            result.reverse()
            self.best_cost = sum(cost[2] for cost in result)
            self.best_solution = result
            return result

        # report if the search has stopped because of the time limit
        if self.status == "stopped" and self.best_solution is None:
            print("Suche mit Zeitlimit ohne Erfolg")

        return [] # return emptylist if nothing found
    