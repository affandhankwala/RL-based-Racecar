import matplotlib.pyplot as plt
from calculations import list_mean
from typing import Dict, List

"""
This file is responsible for the gathering and plotting of racing metrics. 
"""

"""
This list converts a dictionary with the keys 'walls hit', 'moves', and 'time' into
three separate lists and returns those lists. 
"""
def get_lists(metrics: Dict) -> List[List]:
    # Initialize lists
    wall_list = []
    moves_list = []
    times_list = []
    for experiment in metrics.keys():
        # Append all values to their lists respectively
        wall_list.append(metrics[experiment]['walls hit'])
        moves_list.append(metrics[experiment]['moves'])
        times_list.append(metrics[experiment]['time'])
    # Return lists
    return wall_list, moves_list, times_list

"""
This method calculates the average of the 'walls hit', 'moves', and 'time' key values within 
the metrics dictionary. 
"""
# This method calculates the mean of all walls hit, moves, and timing
def get_racer_averages(metrics: Dict, title: str) -> List:
    # Get all respective lists
    wall_list, moves_list, times_list = get_lists(metrics)
    # Get means of all lists
    wall_list_mean = round(list_mean(wall_list), 2)
    moves_list_mean = round(list_mean(moves_list), 2)
    time_list_mean = round(list_mean(times_list), 8)
    # Save into txt file and return
    file_name = f"{title}.txt"
    with open(file_name, "a") as file:
        file.write(f"AVG Walls hit: {wall_list_mean} \n")
        file.write(f"AVG moves: {moves_list_mean} \n")
        file.write(f"AVG time: {time_list_mean} \n")
    return wall_list_mean, moves_list_mean, time_list_mean

"""
This method plots the metrics of the racer. Since we measure the 'walls hit', 'moves', and 'time'
of each experiment, we create three subplots that measure each value. We also save all the averages
and 
"""
def plot_metrics(metrics: Dict, title: str) -> None: 
    # Get respective lists
    wall_list, moves_list, times_list = get_lists(metrics)
    # Instantiate Experiment counts as x values [1 : length]
    x = range(1, len(wall_list) + 1)
    # Create 1 x 3 plot configuration
    fig, axes = plt.subplots(1, 3, figsize = (15, 5))
    # Plot wall_list
    axes[0].plot(x, wall_list, label = 'Walls hit', color = 'blue')
    axes[0].set_title("Walls hit over all Experiments")
    axes[0].set_xlabel("Experiment")
    axes[0].set_ylabel("Walls hit")
    # Plot moves_list
    axes[1].plot(x, moves_list, label = 'Moves', color = 'red')
    axes[1].set_title("Moves made over all Experiments")
    axes[1].set_xlabel("Experiment")
    axes[1].set_ylabel("Moves made")
    # Plot times_list
    axes[2].plot(x, times_list, label = 'Time', color = 'green')
    axes[2].set_title("Time per Experiment")
    axes[2].set_xlabel("Experiment")
    axes[2].set_ylabel("Time")
    # Adjust layout 
    plt.tight_layout()
    # Save plot
    file_name = f"{title}.png"
    plt.savefig(file_name)

