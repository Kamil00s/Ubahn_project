import pandas as pd


def build_graph(path="dataset.csv"):
    graph = {}
    df = pd.read_csv(path, sep=";", decimal=",")
    for _,line in df.iterrows():
        source = line["from"]
        target = line["to"]
        road = {
        "to": line["to"],
        "cost_min": line["cost_min"],
        "action": line["action"],
        "line": line["line"],
        "station": line["station"],
        "from_lon": line["from_lon"],
        "from_lat": line["from_lat"],
        "to_lat": line["to_lat"],
        "to_lon": line["to_lon"], 
        }
        if source not in graph:
            graph[source] = []
        if target not in graph:
            graph[target] = []

        graph[source].append(road)
    print(f"Total nodes: {len(graph)}")
    print(f"Total edges: {sum(len(e) for e in graph.values())}")
    return graph



