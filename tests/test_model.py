import pytest
from pathlib import Path
from graph import build_graph
from model import a_model

DIR = Path(__file__).resolve().parents[1]

@pytest.fixture(scope="module")
def graph():
    return build_graph(DIR / "dataset.csv")

def test_a_walk_fastest(graph):
    # Case a: Laufen geht am schnellsten, aber A* untersucht U-Bahn Pfade
    model = a_model(graph)
    start = (52.5025, 13.3255) # Near Uhlandstraße
    goal = (52.5026, 13.3270)  # Just ~100 meters down the road
    path = model.find_path(start, goal)
    
    assert len(path) == 1
    assert path[0][3] == "walk"
    assert model.states_examined > 1 # Proves A* explored alternatives

def test_b_optimal_no_transfer(graph):
    # Case b: Optimale Lösung beruht auf Fahren ohne Umsteigen
    model = a_model(graph)
    start = (52.5025, 13.325555555)       # Uhlandstraße (U1)
    goal = (52.505083333, 13.449047222)   # Warschauer Straße (U1)
    path = model.find_path(start, goal)
    
    transfers = [step for step in path if step[3] == "transfer"]
    assert len(transfers) == 0

def test_c_optimal_one_transfer(graph):
    # Case c: Optimale Lösung beinhaltet 1x Umsteigen
    model = a_model(graph)
    start = (52.5025, 13.325555555)       # Uhlandstraße (U1)
    goal = (52.486666666, 13.321944444)   # Blissestraße (U7)
    path = model.find_path(start, goal)
    
    transfers = [step for step in path if step[3] == "transfer"]
    assert len(transfers) == 1

def test_d_edge_case_pmax_potentially_not_optimal(graph):
    # Case d: Rathaus Spandau -> Rudow. The whole U7 needs 41 actions, so with
    # p_max=40 paths are dropped and the solution is only potentially optimal.
    model = a_model(graph, p_max=40)
    path = model.find_path((52.535, 13.20027), (52.41583, 13.49611))

    assert len(path) > 0
    assert model.path_limit_reached is True
    assert model.result == "potentially_not_optimal"

def test_e_edge_case_pmax_no_solution(graph):
    # Case e: same pair, p_max=30 -> no route fits into 30 actions
    model = a_model(graph, p_max=30)
    path = model.find_path((52.535, 13.20027), (52.41583, 13.49611))

    assert len(path) == 0
    assert model.result == "no_solution_pmax"

def test_f_edge_case_time_limit(graph):
    # Case f: Kreuzberg -> Altstadt Köpenick (no U-Bahn nearby) needs more than 1 s
    model = a_model(graph, time=1)
    path = model.find_path((52.5052, 13.4262), (52.4447, 13.5745))

    assert model.status == "stopped"
    assert model.result in ("timeout_with_solution", "timeout_no_solution")
