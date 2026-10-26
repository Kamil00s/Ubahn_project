# Multimodal Route Planning – Berlin U-Bahn 🚇

## Overview 🧭

This project implements a multimodal route planner for Berlin Ubahn using the A* search algorithm.

Given arbitrary start and destination coordinates, the program searches for a route that minimizes the estimated total travel time. A route can consist of walking, travelling by underground train, and transferring between U-Bahn lines.

The implementation is based on the U-Bahn network provided in the assignment dataset.

## Features

- Route planning between geographic coordinates.
- Walking connections between the start, U-Bahn stations, and destination.
- U-Bahn connections weighted by travel time.
- Transfer connections with a fixed transfer penalty.
- A* search using a heuristic based on geographic distance.
- Search statistics and route information, where implemented.
- Optional search limits, where implemented.

## Requirements ⚙️
-> requirements.txt

Install the required packages with:

```bash
python -m pip requirements.txt
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
python -m pip install requirements.txt
```

Ensure that the dataset CSV file is available at the path expected by the program.

## Running the program ▶️

Run the project's entry-point script:

```bash
python -m scripts.basic_run start_coordinate1 start_coordinate2 goal_coordinate1 goal_coordinate2
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

Update this section to match the actual repository:

```text
Ubahn_project/
├── dataset.csv
├── model.py
├── graph.py
├── cord.py
├── timer.py
├── tests/
├── scripts/
└── README.md
```

## Limitations ⚠️

The calculated route depends on the provided dataset and the assumptions used by the model. The planner uses fixed walking speed and transfer time and does not model live train schedules, delays, or real-time disruptions.

Search limits may prevent the algorithm from finding a route or proving that a returned route is optimal.

