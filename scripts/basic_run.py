from graph import build_graph
from model import a_model
from cord import find_closest,how_many_meters
from model import a_model
import argparse
from pathlib import Path
from itertools import islice

DIR = Path(__file__).resolve().parents[1]

def pr_float(s):
    return float(s.replace(",", "."))

def main():
    #parser for thescript arguments
    parser = argparse.ArgumentParser(description="Run the pathfinding algorithm.")
    parser.add_argument("s_lat", type=pr_float, help="Latitude of the starting point")
    parser.add_argument("s_lon", type=pr_float, help="Longitude of the starting point")
    parser.add_argument("t_lat", type=pr_float, help="Latitude of the goal point")
    parser.add_argument("t_lon", type=pr_float, help="Longitude of the goal point")
    args = parser.parse_args()

    print(f"Starting point: {args.s_lat}, {args.s_lon}")
    print(f"Goal point: {args.t_lat}, {args.t_lon}")

    graph = build_graph(DIR / "dataset.csv")
    stations = find_closest(graph, args.s_lat, args.s_lon)
    print(f"Closest 5 stations to starting point: {list(islice(stations,5))}")

    meters = how_many_meters(args.s_lat, args.s_lon, args.t_lat, args.t_lon)
    print(f"Distance between starting point and goal point: {meters} meters")

    model = a_model(graph)
    start = args.s_lat, args.s_lon
    goal = args.t_lat, args.t_lon
    result = model.find_path(start,goal)

    print(result)
    print(model.status)
    print(model.run_time)
    print(model.best_cost)

if __name__ == "__main__":
    main()
