from test import test_all

"""
Main Method
"""
def main ():
    # Set up parameter values
    parameters = {
        'directory': "tracks",
        'track_names': ["W-track", "O-track", "L-track", "R-track"],
        'movement_cost': -1,
        'discount': 0.9,
        'threshold': 5, 
        'experiments': 10,
        'eta': 0.05,
        'initial_exploration_rate': 1,
        'episodes': 15000
    }
    # Run all tests and store all results
    test_all(parameters)

if __name__ == "__main__": 
    main() 
