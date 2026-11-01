from graph import build_graph
from model import a_model
from pathlib import Path

DIR = Path(__file__).resolve().parents[1]


def print_path(path):
    for i, (frm, to, cost, action, h) in enumerate(path, 1):
        print(f"  {i:2}. {action:8} {frm} -> {to}  ({cost:.1f} min)")


def run_case(name, graph, start, goal, p_max=40, time_limit=1.0, show_examined=False):
    print(f"\n{'='*60}\nExperiment {name}\n{'='*60}")
    print(f"Start- und Zielkoordinaten: Start {start}, Ziel {goal}")
    print(f"Limits: p_max = {p_max}, Zeitlimit = {time_limit} s")

    model = a_model(graph, p_max=p_max, time=time_limit)
    path = model.find_path(start, goal)

    if path:
        print("Lösungspfad:")
        print_path(path)
        transfers = sum(1 for step in path if step[3] == "transfer")
        print(f"Gesamtreisezeit: {model.best_cost:.1f} min, {len(path)} Aktionen, {transfers} Umstieg(e)")
    else:
        print("Kein Lösungspfad gefunden.")

    print(f"Ergebnis: {model.result}")
    print(f"Speicherverbrauch (maximale Pfade in sortierter Liste): {model.max_open_size}")
    print(f"Anzahl untersuchter Zustände: {model.states_examined}")
    print(f"Laufzeit: {model.run_time:.2f} s")
    if show_examined:
        print("Beispiele untersuchter Zustände (Knoten, Pfadlänge, g, f):")
        for example in model.examined_examples:
            print(f"  {example}")


def main():
    graph = build_graph(DIR / "dataset.csv")

    # a) Brandenburger Tor -> Potsdamer Platz: walking (9 min) is fastest
    run_case("a) Walk fastest", graph, (52.5163, 13.3777), (52.5096, 13.3760), show_examined=True)
    # b) Uhlandstraße -> Warschauer Straße: whole U1, no transfer
    run_case("b) No transfer", graph, (52.5025, 13.32555), (52.50508, 13.44904))
    # c) Uhlandstraße -> Blissestraße: U9, transfer at Berliner Straße, U7
    run_case("c) One transfer", graph, (52.5025, 13.32555), (52.48666, 13.32194))
    # d) Rathaus Spandau -> Rudow: whole U7 needs 41 actions, p_max = 40
    run_case("d) p_max potentially not optimal (p_max=40)", graph,
             (52.5350, 13.20027), (52.41583, 13.49611), p_max=40)
    # e) same pair, p_max = 30: no route fits into 30 actions
    run_case("e) p_max no solution (p_max=30)", graph,
             (52.5350, 13.20027), (52.41583, 13.49611), p_max=30)
    # f) Kreuzberg -> Altstadt Köpenick (no U-Bahn nearby): search needs > 1 s
    run_case("f) Time limit (1 s)", graph, (52.5052, 13.4262), (52.4447, 13.5745))


if __name__ == "__main__":
    main()
