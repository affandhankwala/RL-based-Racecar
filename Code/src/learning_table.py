from calculations import convert_list_to_coordinate
from track import Track
from racecar import Racecar
from typing import Dict, List


"""
This file acts as a helper for the initialization of value dictionaries for both value iteration and the Q 
learner algorithms. 
"""

"""
Initialize a dictionary to model the track. Each position on the track shall be set as a coordinate in 
the string format "[x, y]". Each coordinate shall have a couple member keys. The 'reward' member key
stores the base reward for each position. Walls and Finish positions shall have the parameterized rewards.
The starting line and any empty position has a reward of movement cost--as it would cost that much to move
to those locations. Each state is also given a 'changeable' member key which indicates whether the rewards
(not base rewards) can be altered at said location. The dictionary is returned. 
"""
# Initialize a dictionary to model rewards of track
def initialize_value_dict (track: Track, wall_reward: float, finish_reward: float, movement_cost: float) -> Dict:
    # Create a starter value dictionary where all track positions have base rewards
    # Get the track in array format
    track_array = track.track_list
    # Initialize value dict
    value_dict = {}
    # Iterate through all track positions
    for row in range(len(track_array)): 
        for col in range(len(track_array[row])):
            # Store the state space
            location = convert_list_to_coordinate([row, col])
            current_position = track_array[row][col]
            # Determine which type the state is
            # If position is a wall, set reward to wall_reward and set as unchangeable
            value_dict[location] = {}
            if current_position == '#':
                value_dict[location]['reward'] = wall_reward
                value_dict[location]['changeable'] = False
            # If position is finish line, set reward to finish_reward and set as unchangeable
            elif current_position == 'F':
                value_dict[location]['reward'] = finish_reward
                value_dict[location]['changeable'] = False
            # If position is road or start, set reward to movement cost and set as changeable
            elif current_position == 'S' or current_position == '.':
                value_dict[location]['reward'] = movement_cost
                value_dict[location]['changeable'] = True
            else:
                print("Invalid character found within track")
                return None
            # Add visit counter
            value_dict[location]['visit_count'] = 0
    # Return the value dictionary
    return value_dict

"""
Run the racer with the passed in parameters and determine where it ends up via the racer's pseudo_run method. 
If we hit a wall, return the wall's reward and similarly if we finished, return the finish's reward. 
If we ended up at another location, we return the reward at the ending state. If the ending state is 
not the exact same as the starting state and has been explored and we do not wish to get the base reward, we
return the 'previous reward' of that state. This is utilized in the value_iteration algorithm. If those 
previous conditions are not met, we return the base reward of that position. 
"""
def get_reward_from_accelerating(racer: Racecar, position: List, velocity: List, acceleration: List,
                                 wall_reward: int, finish_reward: int, value_dict: Dict, base_reward: bool) -> float:
    prev_path = racer.previous_path
    prev_pos = racer.previous_position
    ending_location = racer.psuedo_run(position, velocity, acceleration)
    # Reset Racer
    racer.reset_p_v(position, velocity, prev_path, prev_pos)
    # Check what ending location is
    if ending_location == 'wall': 
        return wall_reward
    elif ending_location == 'finish':
        return finish_reward
    else:
        # If we didn't hit wall or finish, we retrieve the coordinates of the ending location
        p, v = ending_location
        end_position = convert_list_to_coordinate(p)
        end_velocity = convert_list_to_coordinate(v)
        # If we have already explored that area, we should retreive the reward of our final velocity
        # Also verify that ending position is not the same as starting position v = 0,0 and a = 0,0
        # Return the base reward if base_reward is set to True
        if (end_velocity in value_dict[end_position] and
            end_position != convert_list_to_coordinate(position) and
            base_reward is False):
            # If we have already explored, we are guaranteed to have previous reward
            # Use the previous reward when within the same iteration
            return value_dict[end_position][end_velocity]['previous reward']
        # If we have not explored or we wish to get base reward, get base reward minus the amount of times we have visited
        else:
            return value_dict[end_position]['reward'] - value_dict[end_position]['visit_count']
    
"""
Resets the visit count of every position on track within dictionary
"""
def reset_visits(value_dict: Dict) -> None:
    for key in value_dict.keys():
        # Set the 'visit_count' key to 0
        value_dict[key]['visit_count'] = 0