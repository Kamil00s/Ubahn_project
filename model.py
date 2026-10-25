import pandas as pd
import heapq
from geopy.distance import geodesic
from timer import timer

class a_model:
    
    def __init__(self, graph, time=2, v_max=80):
        self.WALK_SPEED = 5
        self.graph = graph
        self.status = "idle"
        self.max_time = time
        self.v_max = v_max
        self.coords = {}
        self.run_time = 0.0
        self.best_cost = 0.0
        for s, travels in self.graph.items():
            for t in travels:
                self.coords[s] = (t["from_lat"], t["from_lon"])
                self.coords[t["to"]] = (t["to_lat"],t["to_lon"])
    

    def heuristic(self, a,b):
        #calculate the distance to place km/s
        dist = geodesic(a, b).meters / 1000
        cost = (dist / self.v_max) * 60
        return cost

    def get_neighbors(self,position):
        #findneighbors in graph - all travels possible
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
        #find distance between two points
        dist = geodesic((lat1,lon1),(lat2,lon2)).meters / 1000
        return dist

    def walk_min(self,a,b):
        return self.walking_distance_km(a[0],a[1],b[0],b[1]) / self.WALK_SPEED * 60
    

    #calculate all the moves possible
    def get_moves(self,node,goal):
        #moves = tuples: (node_from, node_to, cost_min, action, heuristics)
        
        moves = []
        if node == "START":
            #walk straight to the goal 
            moves.append((node, "GOAL", self.walk_min(self.coords[node], goal), "walk", 0))
            #walk to every station 
            for n in self.graph:
                moves.append((node, n, self.walk_min(self.coords[node], self.coords[n]), "walk",
                              self.heuristic(self.coords[n], goal)))
        #travel or transfer 
        else:
            
            #
            for d in self.get_neighbors(node):
                moves.append((node, d["to"], d["cost_min"], d["action"],
                              self.heuristic(self.coords[d["to"]], goal)))
            #walk from the station to the goal
            moves.append((node, "GOAL", self.walk_min(self.coords[node], goal), "walk", 0))
        return moves

    @timer
    def find_path(self, start, goal):
        # node = station and line, additional signs are "START" and "GOAL"
        # move tuple = (node_from, node_to, cost_min, action, heuristics)
        #start, goal = (lat,lon) 

        #set the start and goal in coords dict
        self.coords["START"] = start 
        self.coords["GOAL"] = goal

        #
        open_list = [(0, 0, "START")]      # (function, cost before, node), smallest f wins
        best_g = {"START": 0}              # cheapest known cost to node
        parent = {"START": None}            #a chain of nodes (the travel path) 
 
        while open_list and self.status == "searching":
            # we use heapq that outputs node with the lowest f
            f, g, node = heapq.heappop(open_list)
            #skip if not worth checking( we have a cheaper way to get to the node)
            if g > best_g[node]:
                continue                        

            # algorithm found goal -> reverse and return the path
            if node == "GOAL":
                result = []
                while parent[node] is not None:
                    result.append(parent[node])
                    node = parent[node][0]
                result.reverse() # reverse the list 
                self.best_cost = sum(cost[2] for cost in result)
                return result

            #try all moves from this node if its not goal
            for move in self.get_moves(node, goal):
                _, nxt, cost, _, h = move
                new_g = g + cost
                # keep only if cheaper than we had before, if we dont have it yet saved compare to inf
                if new_g < best_g.get(nxt, float("inf")):
                    best_g[nxt] = new_g
                    parent[nxt] = move
                    heapq.heappush(open_list, (new_g + h, new_g, nxt))
 
        return [] #return emptylist if nothing found 
        