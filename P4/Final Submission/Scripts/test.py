from racecar import Racecar
from track import Track
from value_iteration import Value_Iteration
from learning_model import Learning_Model
from calculations import convert_list_to_coordinate
from gather_metrics import get_racer_averages, plot_metrics
import time
from typing import Dict

"""
Gather all metrics from the Racecar and alter the dictionary in memory
"""
def gather_metrics(metrics: Dict, experiment_name: str, racer: Racecar, time: time) -> None:
    # Alter the dictionary in memory
    metrics[experiment_name]['walls hit'] = racer.get_wall_hit_count()
    metrics[experiment_name]['moves'] = racer.get_moves()
    metrics[experiment_name]['time'] = time

"""
Test the value iteration model via the passed in parameters. First train the model and then test the model. 
Testing is done by creating a Racecar object and navigating it through the track via the model's stored
value dict. This is done for a specified number of experiments and the metrics are stored and presented in 
nominal and visual format. Debug mode possible. 
"""
def test_value_iteration(directory: str, track_name: str, movement_cost: float, 
                         discount: float, threshold: float, max_experiments: int, restart: bool,
                         debug = False) -> None:
    print(f"Training Value Iteration on track {track_name} with Restart: {restart}")
    # Define a track Object
    track = Track(directory, track_name)
    # Define a Value Iteration Object
    v = Value_Iteration(track, movement_cost)
    # Train the Value Iteration object
    start_time = time.time()
    training_episodes = v.train(discount, threshold, debug)
    end_time = time.time()
    training_time = end_time - start_time
    # Define metrics dictionary
    metrics = {}
    # Iterate through n experiments
    experiment_count = 1
    while experiment_count <= max_experiments:
        if debug: experiment_name = f"Experiment {experiment_count}"
        # Define dictionary for experiment
        metrics[experiment_name] = {}
        # Define a race car
        racer = Racecar(track)
        # Start timer
        start_time = time.time()
        # Test the model
        v.test(racer, restart)
        # Store metrics
        end_time = time.time()
        gather_metrics(metrics, experiment_name, racer, end_time - start_time)
        if debug: print(f"Completed Experiment {experiment_count}")
        experiment_count += 1
    # Print all metrics and display them
    title = f"{track_name}_VIteration_Restart_{restart}"
    
    # Print training metrics
    with open (f"{title}.txt", "w") as file:
        file.write(f"Training Episodes: {training_episodes} \n")
        file.write(f"Training time: {training_time} \n")
        
    get_racer_averages(metrics, title)
    plot_metrics(metrics, title)

"""
Test the Q learner model via the passed in parameters. First train the model and then test the model similarly 
to testing the value iteration model. One of the parameter controls whether our model utilizes SARSA algorithm. 
Debug mode possible. 
"""
def test_Q_learner(directory: str, track_name: str, movement_cost: float, eta: float, discount: float, 
                   exploration_rate: float, threshold: float, episodes: int, max_experiments: int, restart: bool, 
                   sarsa: bool, debug = False):
    print(f"Traing Q Learner on track {track_name} with Restart: {restart} and SARSA: {sarsa}")
    # Define track object
    track = Track(directory, track_name)
    # Define Q Learning Model Object
    Q_model = Learning_Model(track, movement_cost, sarsa)
    # Train Q model
    start_time = time.time()
    training_episodes = Q_model.train(eta, discount, exploration_rate, threshold, episodes, debug)
    end_time = time.time()
    training_time = end_time - start_time
    # Define metrics dictionary
    metrics = {}
    # Iterate through n experiments
    experiment_count = 1
    while(experiment_count <= max_experiments):
        if debug: experiment_name = f"Experiment {experiment_count}"
        # Create racer for experiment
        racer = Racecar(track)
        # Start timer
        start_time = time.time()
        # Test model
        # Tiny exploration rate to avoid stuck
        explore_rate = 0.01
        Q_model.test(racer, restart, explore_rate)
        # End Timer
        end_time = time.time()
        # Gather metrics
        metrics[experiment_name] = {}
        gather_metrics(metrics, experiment_name, racer, end_time - start_time)
        if debug: print(f"Completed Experiment {experiment_count}")
        experiment_count += 1
    # Print all metrics and display
    title = f"{track_name}_QLearn_Restart_{restart}_SARSA_{sarsa}"
    
    # Print training time
    with open (f"{title}.txt", "w") as file:
        file.write(f"Training Episodes: {training_episodes} \n")
        file.write(f"Training time: {training_time} \n")

    get_racer_averages(metrics, title)
    plot_metrics(metrics, title)

"""
Test all models on all tracks under all conditions and store all data. This method is to allow a passive running
of metric gathering across all trackss
"""
def test_all(parameters: Dict) -> None:
    # Unpack parameters
    directory = parameters['directory']
    track_names = parameters['track_names']
    movement_cost = parameters['movement_cost']
    discount = parameters['discount']
    threshold = parameters['threshold']
    experiments = parameters['experiments']
    eta = parameters['eta']
    initial_exploration_rate = parameters['initial_exploration_rate']
    episodes = parameters['episodes']

    debug = True
    test_Q_learner(directory, "L-track", movement_cost, eta, discount, initial_exploration_rate, threshold, episodes, experiments, False, False, debug)
    # Loop through each track
    for t_name in track_names:        
        # Test Value iteration without restarting
        test_value_iteration(directory, t_name, movement_cost, discount, threshold, experiments, False, debug)
        # Test Value Iteraation with restarting
        test_value_iteration(directory, t_name, movement_cost, discount, threshold, experiments, True, debug)
        # Test Q Learning without restarting without SARSA
        test_Q_learner(directory, t_name, movement_cost, eta, discount, initial_exploration_rate, threshold, episodes, experiments, False, False, debug)
        # Test Q Learning with restating without SARSA
        test_Q_learner(directory, t_name, movement_cost, eta, discount, initial_exploration_rate, threshold, episodes, experiments, True, False, debug)
        # Test Q Learning without restarting with SARSA
        test_Q_learner(directory, t_name, movement_cost, eta, discount, initial_exploration_rate, threshold, episodes, experiments, False, True, debug)
        # Test Q Learning with restarting with SARSA
        test_Q_learner(directory, t_name, movement_cost, eta, discount, initial_exploration_rate, threshold, episodes, experiments, True, True, debug)

