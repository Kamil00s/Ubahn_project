import heapq
from geopy.distance import geodesic
from timer import timer

class a_model:

    def __init__(self, graph, time=1, p_max=40):
        self.WALK_SPEED = 5             # km/h, given by the assignment
        self.MAX_WALK_TIME = 20         # walk to/from stations up to 20 minutes
        self.MIN_NEARBY_STATIONS = 3    # always allow the 3 nearest stations
        self.MAX_DIRECT_WALK_TIME = 60  # walking the whole way only up to 60 minutes
        self.graph = graph
        self.status = "idle"            # set by the timer: searching / stopped / finished
        self.max_time = time            # restriction (2): time limit in seconds
        self.p_max = p_max              # restriction (1): maximum path length
        self.run_time = 0.0
        self.best_cost = 0.0
        self.result = "idle"            # which termination case occurred
        self.coords = {}
        for s, travels in self.graph.items():
            for t in travels:
                self.coords[s] = (t["from_lat"], t["from_lon"])
                self.coords[t["to"]] = (t["to_lat"], t["to_lon"])
        # heuristic speed = fastest straight-line speed of any U-Bahn edge (about 28 km/h)
        self.v_max = self.fastest_speed()

    def fastest_speed(self):
        best = self.WALK_SPEED
        for s, travels in self.graph.items():
            for t in travels:
                if t["action"] == "travel" and t["cost_min"] > 0:
                    km = geodesic(self.coords[s], self.coords[t["to"]]).meters / 1000
                    best = max(best, km / (t["cost_min"] / 60))
        return best

    def walk_min(self, a, b):
        # walking time in minutes between two (lat, lon) points
        return geodesic(a, b).meters / 1000 / self.WALK_SPEED * 60

    def heuristic(self, a, b):
        # estimate the remaining travel time using straight-line distance and maximum speed
        return geodesic(a, b).meters / 1000 / self.v_max * 60

    def nearby_nodes(self, point):
        # all platforms within MAX_WALK_TIME, plus the platforms of the 3 nearest stations
        times = {n: self.walk_min(point, self.coords[n]) for n in self.graph}
        station_time = {}
        for n, t in times.items():
            station = n.split(":", 1)[1]
            station_time[station] = min(t, station_time.get(station, float("inf")))
        nearest = sorted(station_time, key=station_time.get)[:self.MIN_NEARBY_STATIONS]
        return {n: t for n, t in times.items()
                if t <= self.MAX_WALK_TIME or n.split(":", 1)[1] in nearest}

    # calculate all the moves possible
    def get_moves(self, node, goal):
        # moves = tuples: (node_from, node_to, cost_min, action, heuristics)
        moves = []
        if node == "START":
            # walking the whole way is allowed up to MAX_DIRECT_WALK_TIME
            direct_walk_time = self.walk_min(self.coords[node], goal)
            if direct_walk_time <= self.MAX_DIRECT_WALK_TIME:
                moves.append((node, "GOAL", direct_walk_time, "walk", 0))
            # walk to nearby stations (computed once in find_path)
            for n, station_walk_time in self.access.items():
                moves.append((node, n, station_walk_time, "walk", self.heuristic(self.coords[n], goal)))
        else:
            # travel or transfer, as given in the dataset
            for edge in self.graph[node]:
                moves.append((node, edge["to"], edge["cost_min"], edge["action"],
                              self.heuristic(self.coords[edge["to"]], goal)))
            # walk from a station near the goal to the goal
            if node in self.egress:
                moves.append((node, "GOAL", self.egress[node], "walk", 0))
        return moves

    def build_path(self, parent, state):
        # follow the parent pointers back to the start and return the moves in order
        result = []
        while parent[state] is not None:
            state, move = parent[state]
            result.append(move)
        result.reverse()
        self.best_cost = sum(move[2] for move in result)
        return result

    @timer
    def find_path(self, start, goal):
        # node = station and line, additional signs are "START" and "GOAL"
        # start, goal = (lat, lon)
        self.coords["START"] = start
        self.coords["GOAL"] = goal
        self.access = self.nearby_nodes(start)   # stations you may walk to from the start
        self.egress = self.nearby_nodes(goal)    # stations you may walk from to the goal

        open_list = [(0, 0, "START", 0)]   # (f, g, node, path_length), smallest f wins
        best_g = {("START", 0): 0}         # cheapest known cost for each node and path length
        parent = {("START", 0): None}      # previous state and move, for path reconstruction

        self.states_examined = 0            # logging: number of examined states
        self.max_open_size = len(open_list) # logging: maximum number of paths in the sorted list
        self.path_limit_reached = False     # was any path dropped because of p_max?
        self.best_goal_state = None         # cheapest goal path generated so far (for the time limit)
        self.examined_examples = []         # a few examined states, shown for use case a)

        while open_list and self.status == "searching":
            f, g, node, length = heapq.heappop(open_list)
            # skip if a cheaper path to this node and length has already been found
            if g > best_g[(node, length)]:
                continue
            self.states_examined += 1
            if node not in ("START", "GOAL") and len(self.examined_examples) < 5:
                self.examined_examples.append((node, length, round(g, 1), round(f, 1)))

            # goal test
            if node == "GOAL":
                result = self.build_path(parent, (node, length))
                # case c): some path was dropped because of p_max -> maybe not optimal
                if self.path_limit_reached:
                    self.result = "potentially_not_optimal"
                    print("potenziell nicht optimale Lösung gefunden")
                # case b): nothing was dropped -> optimal
                else:
                    self.result = "optimal"
                    print("Optimale Lösung gefunden")
                return result

            for move in self.get_moves(node, goal):
                _, nxt, cost, _, h = move
                new_g = g + cost
                new_length = length + 1
                # restriction (1): paths longer than p_max are not inserted, search continues
                if new_length > self.p_max:
                    self.path_limit_reached = True
                    continue
                if new_g < best_g.get((nxt, new_length), float("inf")):
                    best_g[(nxt, new_length)] = new_g
                    parent[(nxt, new_length)] = ((node, length), move)
                    if nxt == "GOAL" and (self.best_goal_state is None
                                          or new_g < best_g[self.best_goal_state]):
                        self.best_goal_state = (nxt, new_length)
                    heapq.heappush(open_list, (new_g + h, new_g, nxt, new_length))
                    self.max_open_size = max(self.max_open_size, len(open_list))

        # case a): the sorted list ran empty
        if self.status == "searching" and not open_list:
            if self.path_limit_reached:
                self.result = "no_solution_pmax"
                print("Lösung mit begrenztem Speicher nicht generierbar")
                print("mit der maximalen Pfadlänge kann eine Lösung nicht generiert werden")
            else:
                self.result = "no_route"
                print("Keine Route gefunden")
            return []

        # restriction (2): time limit reached -> best solution found so far, if any
        print(f"Zeitlimit von {self.max_time} s erreicht")
        if self.best_goal_state is not None:
            self.result = "timeout_with_solution"
            print("Beste bisher gefundene Lösung (nicht als optimal nachgewiesen)")
            return self.build_path(parent, self.best_goal_state)

        self.result = "timeout_no_solution"
        print("Suche mit Zeitlimit ohne Erfolg")
        return []
