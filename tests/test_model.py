from pathlib import Path
import pytest
from graph import build_graph
from model import a_model

DIR = Path(__file__).resolve().parents[1]

@pytest.fixture(scope="module")
def prepare():
    graph = build_graph(DIR / "dataset.csv")
    return a_model(graph)


@pytest.mark.parametrize("a1, a2, b1, b2, expected",[
        # 1. walking 
        (52.5219, 13.4132, 52.5225, 13.4150,1),

        # 2. one line – U1
        # Uhlandstraße -> Warschauer Straße
        (52.5025, 13.325555555, 52.505083333, 13.449047222,11),

        # 3. one transfer– U1 -> U7
        # transfer at Möckernbrücke
        (52.5025, 13.325555555, 52.486666666, 13.321944444,7),
])


def test_run(prepare,a1,a2,b1,b2,expected):
    start = a1,a2
    goal = b1,b2
    assert len(prepare.find_path(start,goal)) == expected

