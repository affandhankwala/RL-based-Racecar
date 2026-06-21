# RL-based Racecar

A reinforcement-learning project that teaches a racecar to drive a track as fast as possible, comparing
**Value Iteration**, **Q-Learning**, and **SARSA** across several track layouts.

## Introduction

This project was completed for Johns Hopkins University's *Introduction to Machine Learning* course
(605.649).

## Problem Statement

Given a track represented as a 2D grid of characters, the goal is to train an agent that drives a racecar
optimally from the start line to the finish line.

The car's state consists of:

- **Position** $(x_t, y_t)$ — a coordinate on the track.
- **Velocity** $(v_{x_t}, v_{y_t})$ — bounded to $[-5, +5]$ on each axis.
- **Acceleration** $(a_{x_t}, a_{y_t})$ — the only thing the agent controls.

Each acceleration component can be set to `-1`, `0`, or `+1` per step. When the car hits a wall it is
reset either to the **nearest track cell to the impact** or to the **starting line**, depending on a
configurable crash flag.

## Methodology

Three control algorithms are implemented and compared:

- **Value Iteration** — model-based dynamic programming.
- **Q-Learning** — off-policy temporal-difference control.
- **SARSA** — on-policy temporal-difference control.

Each agent is evaluated on the four provided tracks — **L**, **O**, **R**, and **W** — under both crash
behaviours (reset-to-nearest vs. reset-to-start).

## Repository Structure

```
RL-based-Racecar/
├── README.md
├── Report.pdf                       # Full report
└── Code/
    ├── data.xlsx                    # Tabulated results
    ├── src/
    │   ├── main.py                  # Entry point: configures parameters and runs all tests
    │   ├── test.py                  # Drives experiments across tracks / algorithms
    │   ├── track.py                 # Track loading and representation
    │   ├── racecar.py               # Racecar dynamics (position / velocity / acceleration)
    │   ├── value_iteration.py       # Value Iteration solver
    │   ├── learning_model.py        # Q-Learning / SARSA training
    │   ├── learning_table.py        # Q-table representation
    │   ├── calculations.py          # Shared math helpers
    │   ├── gather_metrics.py        # Metric collection
    │   └── print_track.py           # Track / policy visualization
    ├── tracks/                      # L / O / R / W track text files
    └── visualized_results/          # Per-track, per-algorithm result plots and logs
```

## Running

```bash
cd Code/src
python main.py
```

Experiment parameters — tracks to run, discount, exploration rate, episode count, number of experiments,
etc. — are set in the `parameters` dictionary in `main.py`. Results and visualizations are written to
`Code/visualized_results/`.

### Requirements

- Python 3
- `numpy`, `matplotlib` (and `openpyxl` for the spreadsheet output)

## Results

**Value Iteration produced the fastest race times** overall. Q-Learning was occasionally quicker but far
more variable, generally trailing Value Iteration, and SARSA was the slowest of the three. See
[`Report.pdf`](Report.pdf) for the full analysis, and `Code/visualized_results/` for per-track learned
policies and lap-time results.
