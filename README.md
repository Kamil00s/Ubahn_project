# Multimodal Route Planning – Berlin U-Bahn 🚇

## Overview 🧭

This project implements a multimodal route planner for Berlin Ubahn using the A* search algorithm.

Given arbitrary start and destination coordinates, the program searches for a route that minimizes the estimated total travel time. A route can consist of walking, travelling by underground train, and transferring between U-Bahn lines.

## Features

- Route planning between geographic coordinates.
- Walking connections between the start, U-Bahn stations, and destination.
- U-Bahn connections weighted by travel time.
- Transfer connections with a fixed transfer penalty.
- A* search using a heuristic based on geographic distance.
- Search statistics: maximum size of the sorted list, number of examined states, runtime.
- Search limits: maximum path length `p_max` (default 40 actions) and time limit (default 1 s).

## Requirements ⚙️
-> requirements.txt

Install the required packages with:

```bash
python -m pip install -r requirements.txt
```


## Setup 🛠️

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Ubahn_project
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Ensure that the dataset CSV file is available at the path expected by the program.

## Running the program ▶️

Run the project's entry-point script:

Run all commands from the project root.

Single route (start latitude, start longitude, goal latitude, goal longitude):

```bash
python -m scripts.basic_run 52.5025 13.32555 52.50508 13.44904
```

All use cases (a-c) and edge cases (d-f) from the assignment:

```bash
python -m scripts.run_experiments
```

Tests:

```bash
python -m pytest
```

## Route cost model

The total route cost is measured in minutes.

| Action | Cost |
|---|---|
| Walking | Geographic distance divided by 5 km/h |
| U-Bahn travel | Travel time specified in the dataset |
| Transfer | 5 minutes per transfer |

## Algorithm 🧠

The route network is represented as a graph. Stations or station-line combinations are states, and connections between them are actions with associated travel costs.

A* evaluates states using:

`f(n) = g(n) + h(n)`

where:

- `g(n)` is the travel time accumulated from the start to the current state.
- `h(n)` is the heuristic estimate of the remaining travel time.
- `f(n)` is the estimated total cost of a route through that state.

The algorithm maintains a priority queue of candidate states and tracks the lowest known cost of reaching each state.

## Project structure

```text
Ubahn_project/
├── dataset.csv
├── model.py
├── graph.py
├── cord.py
├── timer.py
├── tests/
│   └── test_model.py
├── scripts/
│   ├── basic_run.py
│   └── run_experiments.py
└── README.md
```

## Limitations ⚠️

The calculated route depends on the provided dataset and the assumptions used by the model. The planner uses fixed walking speed and transfer time and does not model live train schedules, delays, or real-time disruptions.

Search limits may prevent the algorithm from finding a route or proving that a returned route is optimal.

Walking from the start / to the goal is allowed to every station within 20 minutes, and always to the 3 nearest stations. Walking the whole way is allowed up to 60 minutes.

