from racecar import Racecar
from track import Track
from calculations import get_max_from_subset, convert_coordinate_to_list, convert_list_to_coordinate
from learning_table import initialize_value_dict, get_reward_from_accelerating
from print_track import print_racer_on_track
from typing import List, Dict

"""
This class creates the Value Iteration model that trains a dictionary with a best action per state to allow a Racecar
to navigate any track. 
"""
  
class Value_Iteration:
    def __init__ (self, track: Track, movement_cost: float):
        self.track = track
        """
        Initialize dictionary to hold all initial rewards at each state. At the start, each position 
        shall be considered a state. However, unique accelerations at each each velocity will be considered
        states during the training process. Since each velocity can have up to 9 unique acceleration values 
        (-1, 0, 1 for both x and y coordinates) and each location can have 121 unique velocities (-5:5 for both
        x and y), each position on the track can have a maximum of 1089 states.
        """ 
        self.value_dict = initialize_value_dict(track, self.get_wall_reward(), self.get_finish_reward(), movement_cost)

    """
    Getter
    """
    def get_value_dict(self) -> Dict:
        return self.value_dict
    
    """
    Get Wall Reward. Hard coded to -1000
    """
    def get_wall_reward(self) -> int: 
        return -1000
    
    """
    Get Finish Reward. Hard coded to 100
    """
    def get_finish_reward(self) -> int:
        return 100
    
    """
    Train will alter the value_dict member variable to have a best action per each state. This is done by going through
    each location on the track and determining the rewards for selecting each acceleration at each velocity. Once the best
    acceleration for each state is selected, it is stored within the dictionary. Once we store the best acceleration for 
    all locations on the track, we consider this to be one episode. We keep running episodes and store the largest change in 
    best value for any state. Once the largest change becomes smaller than our threshold value, we consider the model to be
    trained and end the training process. We also only alter the values of changeable states. Meaning, we do not change
    the values of walls nor finish points. 
    """
    def train (self, discount: float, threshold: float, debug = False) -> int:
        # Develop rewards for each state for each speed. 
        # Initialize biggest delta as low number. It represents maximum difference in state rewards
        biggest_delta = -99999
        # Keep training until magnitude of delta < threshold
        # Counter for metrics
        episode_count = 0
        while (abs(biggest_delta) > threshold): 
            episode_count += 1
            # Re initialize delta
            biggest_delta = -99999
            # Iterate through each element in the track
            track = self.track.track_list
            for row in range(len(track)):
                for col in range(len(track[row])):
                    # Check if the current state's value is changeable
                    location = convert_list_to_coordinate([row, col])
                    if self.value_dict[location]['changeable'] == False:
                        # If not changeable, we move on to next position
                        continue
                    # Iterate through all possible velocities at position and all accelerations and calcualte 
                    # Reward of each possible outcome and store best reward and best acceleration
                    v_row = -5
                    while (v_row < 6):
                        v_col = -5
                        while(v_col < 6):
                            # Create velocity dictionary
                            velocity_pair = convert_list_to_coordinate([v_row, v_col])
                            # Create empty dictionary if velocity_pair doesn't exists
                            if velocity_pair not in self.value_dict[location]:
                                self.value_dict[location][velocity_pair] = {}
                            # Check all 9 acceleration possibilities
                            a_row = -1
                            while(a_row < 2):
                                a_col = -1
                                while(a_col < 2):
                                    # Create acceleration value holder
                                    acceleration_pair = convert_list_to_coordinate([a_row, a_col])
                                    # Create a racecar object for the sake of method utilization
                                    racer = Racecar(self.track)
                                    # Set the position and v
                                    position = [row, col]
                                    velocity = [v_row, v_col]
                                    acceleration = [a_row, a_col]
                                    # Get next_value for accelerating at specific acceleration
                                    next_value = get_reward_from_accelerating(racer, position, velocity, acceleration, 
                                                                          self.get_wall_reward(), self.get_finish_reward(),
                                                                          self.value_dict, False)
                                    # Calculate value as reward(current) + discount * reward(next state)
                                    value = self.value_dict[location]['reward'] + discount * next_value
                                    # Store value within value dict
                                    self.value_dict[location][velocity_pair][acceleration_pair] = value
                                    # Increment acceleration metrics
                                    a_col += 1
                                a_row += 1
                            # Reassign the velocity dictionary as the maximum value and acceleration pair in dictionary
                            best_acceleration = get_max_from_subset(self.value_dict[location][velocity_pair], ['best acceleration', 'best reward', 'previous reward'])
                            best_reward = self.value_dict[location][velocity_pair][best_acceleration]
                            # Store previous reward for delta calculations
                            previous_reward = 0
                            if 'best reward' in self.value_dict[location][velocity_pair]:
                                previous_reward = self.value_dict[location][velocity_pair]['best reward']
                            self.value_dict[location][velocity_pair]['best acceleration'] = convert_coordinate_to_list(best_acceleration)
                            self.value_dict[location][velocity_pair]['best reward'] = best_reward
                            # Update previous reward
                            self.value_dict[location][velocity_pair]['previous reward'] = previous_reward
                            # Update biggest delta if necessary
                            delta = abs(best_reward - previous_reward)
                            if delta > biggest_delta:
                                biggest_delta = delta
                            v_col += 1
                        v_row += 1
                    # Now each velocity pair has a best acceleration and best reward associaated with 
            # All cells have been iterated through
            if debug: print(f"Value Iteration Training Episode: {episode_count} | Max Delta: {biggest_delta}")
        # Threshold has been hit
        # Return episode count for metrics
        return episode_count

    """
    Test runs the supplied Racecar through the value dict until it reaches the finish line. All velocity and position 
    updating is handled within the Racercar's traverse method. Metrics are stored within the Racecar. 
    """
    def test(self, racer: Racecar, restart: bool) -> None:
        while racer.finished() == False:
            # Get current position and velocity
            # Convert position and velocity to string format
            current_position_str = convert_list_to_coordinate(racer.get_position())
            current_velocity_str = convert_list_to_coordinate(racer.get_velocity())
            # Determine what is the best action to take at position and velocity
            best_acceleration = self.value_dict[current_position_str][current_velocity_str]['best acceleration']
            # Traverse the racecar with respective restarting condition
            print_racer_on_track(self.track.track_list, racer.get_position())
            racer.traverse(best_acceleration, restart)
