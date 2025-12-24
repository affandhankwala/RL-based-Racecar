from track import Track
from racecar import Racecar
from learning_table import initialize_value_dict, get_reward_from_accelerating, reset_visits
from calculations import convert_list_to_coordinate, weighted_random
from print_track import print_racer_on_track
import random
from typing import List, Dict

"""
This class is responsible for training a model via the Q learning algorithm. SARSA can be toggled
via a member variable boolean. 
"""
class Learning_Model:
    def __init__(self, track: Track, movement_cost: float, sarsa: bool) -> None:
        self.track = track
        """
        Initialize dictionary to hold all initial rewards at each state. At the start, each position 
        shall be considered a state. However, unique accelerations at each each velocity will be considered
        states during the training process. Since each velocity can have up to 9 unique acceleration values 
        (-1, 0, 1 for both x and y coordinates) and each location can have 121 unique velocities (-5:5 for both
        x and y), each position on the track can have a maximum of 1089 states.
        """ 
        self.value_dict = initialize_value_dict(track, self.get_wall_reward(), self.get_finish_reward(), movement_cost)
        # Initialize whether we plan on doing sarsa
        self.sarsa = sarsa

    """
    Getter
    """
    def get_value_dict(self) -> Dict:
        return self.value_dict
    
    """
    Get Wall Reward. Hard coded to -1000.
    """
    def get_wall_reward(self) -> int:
        return -1000

    """
    Get Finish Reward. Hard coded to 100.
    """
    # Get Finish reward
    def get_finish_reward(self) -> int:
        return 100

    """
    This method looks within the value dictionary at the particular location, velocity 
    and acceleration and returns whether we have a stored 'q_value' key. If not, we 
    return the base reward of that location. 
    """
    # Get Q value of any state
    def get_Q_value(self, position: List, velocity: List, acceleration: List) -> float:
        # Convert position and velocity values
        position_str = convert_list_to_coordinate(position)
        velocity_str = convert_list_to_coordinate(velocity)
        acceleration_str = convert_list_to_coordinate(acceleration)
        # Determine if we have even explored the velocity at specified position
        if velocity_str in self.value_dict[position_str]:
            # Determine if we have explore the acceleration within the velocity state
            if acceleration_str in self.value_dict[position_str][velocity_str]:
                # Return the q_value
                return self.value_dict[position_str][velocity_str][acceleration_str]['q_value']
        # If any conditions fails, return base reward
        return self.value_dict[position_str]['reward']
    
    """
    Return the acceleration state with the best q score given a racer. This is done
    by looping through all possible accelerations and retaining the highest base reward
    of the next action as well as the acceleration to get the racer to the best base
    reward.
    """
    # Return the state (acceleration) with the best q score
    def exploit(self, racer: Racecar) -> List:
        current_position = racer.get_position()
        current_velocity = racer.get_velocity()
        # Look at all possible actions (all acceleration possibilities) and find best reward
        best_reward = -99999
        best_acceleration = None
        a_row = -1
        while a_row < 2:
            a_col =-1
            while a_col < 2:
                acceleration = [a_row, a_col]
                # Get the base reward of particular acceleration
                reward = get_reward_from_accelerating(racer, current_position, current_velocity,
                                                        acceleration, self.get_wall_reward(),
                                                        self.get_finish_reward(), self.value_dict,
                                                        True)
                # Determine if this is the best reward that we have encountered at this state
                if reward > best_reward:
                    # Only save as best acceleration if we are actuall moving a!=0,0 while v==0,0
                    if current_velocity == [0, 0] and acceleration == [0, 0]:
                        # Skip this iteration
                        pass
                    else:
                        best_reward = reward
                        best_acceleration = acceleration
                a_col += 1
            a_row += 1
        return best_acceleration, best_reward
    
    """
    Select a random acceleration (as long as the racer moves) and determine the reward
    of the random acceleration. 
    """
    def explore(self, racer: Racecar) -> List:
        current_position = racer.get_position()
        current_velocity = racer.get_velocity()
        # If velocity is [0,0] make sure not to set acceleration to [0,0]
        if current_velocity == [0, 0]:
            best_acceleration = [0, 0]
            # Re-select acceleration if we end up with no acceleration and no velocity
            while best_acceleration == [0, 0]:
                best_acceleration = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
        else:
            best_acceleration = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
        # Determine reward after this acceleration
        best_reward = get_reward_from_accelerating(racer, current_position, current_velocity,
                                                best_acceleration, self.get_wall_reward(), 
                                                self.get_finish_reward(), self.value_dict, 
                                                True)
        return best_acceleration, best_reward
    
    """
    Return the acceleration and reward of action based on either exploitation or exploration
    policy dependent on the exploration_rate float value. 
    """
    def explore_or_exploit(self, racer: Racecar, exploration_rate: float) -> List:
        # Determine if we exploit or explore
        explore = weighted_random([exploration_rate, 1 - exploration_rate])
        if explore:
            return self.explore(racer)
        else:
            return self.exploit(racer)

    """
    Train allows the value dict class member variable to be sufficiently trained untill our detla value cross aa threshold
    value such that a racer can sufficiently navigate the track in an efficient manner. This is 
    done by initiating a racecar at the starting line of the track. The racer navigates the track via Q learning
    with either SARSA enabled or disabled. The racer shall reset it's position if it hits a wall and the iteration
    completes once it passes the finish line. Once the racer passes the finish line, we decay our exploration
    rate by a certain proportion to slowly encorporate more exploitation tactics. The decay rate is hypertuned to 
    minimize runtime while allowing convergence. Once the episodes are complete, our value dict contains the 
    best acceleration at each state and our model is ready for testing. Debug mode possible.
    """      
    # Model rewards of the track and determine best acceleration at each velocity at each state via Q learning/SARSA
    def train(self, eta: float, discount: float, exploration_rate: float, threshold: float, episodes: int, debug = False) -> int:
        # Initialize biggest delta as maximum difference in Q value among all states within episode
        biggest_delta = -99999
        # Keep counter for metrics
        episode_count = 0
        # Keep learning for set number of episodess. 
        while(abs(biggest_delta) > threshold and episode_count < episodes):
            episode_count += 1
            if debug: print(f"Episode {episode_count} | Biggest Delta: {biggest_delta} | Exploration Rate: {exploration_rate} | SARSA: {self.sarsa}")
            # Re initialize biggest delta
            biggest_delta = -99999
            # Reset visitation count 
            reset_visits(self.value_dict)
            # Create race car that starts at start of track
            racer = Racecar(self.track)
            if episode_count == 70:
                print('here')
            # Traverse the map until we reach the finish line
            while racer.finished() is False:

                """
                Determine where the racer is and move it to the next position based on the explore or exploit policy.
                """

                # Get the current position of racer
                current_position = racer.get_position()
                current_position_str = convert_list_to_coordinate(current_position)
                # Get current velocity of racer
                current_velocity = racer.get_velocity()
                current_velocity_str = convert_list_to_coordinate(current_velocity)
                # Get next state and associated reward
                best_acceleration, best_reward = self.explore_or_exploit(racer, exploration_rate)
                best_acceleration_str = convert_list_to_coordinate(best_acceleration)
                # Apply best acceleration to the racecar
                racer.set_acceleration(best_acceleration)
                # Update velocity and position. This shall be the transition to the 'next state'. 
                racer.update_velocity()
                racer.update_position()
                # Increment visit count of position
                self.value_dict[current_position_str]['visit_count'] += 1

                """
                Update the current position's Q value within the value dict 
                """

                # Determine if we have an current Q value at this state
                current_q = self.get_Q_value(current_position, current_velocity, best_acceleration)
                # Get the next state values
                next_position = racer.get_position()
                next_velocity = racer.get_velocity()
                next_position_str = convert_list_to_coordinate(next_position)
                next_velocity_str = convert_list_to_coordinate(next_velocity)
                # For SARSA learning, determine next q value based on next state's selected action
                if self.sarsa:
                    # Convert the next move's acceleration segment into a string
                    next_best_acceleration_str = convert_list_to_coordinate(self.explore_or_exploit(racer, exploration_rate)[0])
                    # Apply acceleration 
                    prev_path = racer.previous_path
                    prev_pos = racer.previous_position
                    racer.update_velocity()
                    racer.update_position()
                    # Get next next metrics
                    next_next_position_str = convert_list_to_coordinate(racer.get_position())
                    next_next_velocity_str = convert_list_to_coordinate(racer.get_velocity())
                    # Determine if the best_acceleration state has an associated q value
                    # If we finished, return finish reward
                    if racer.finished():
                        next_q_value = self.get_finish_reward()
                    # If we hit wall, return wall reward
                    elif racer.hit_wall() is not None:
                        next_q_value = self.get_wall_reward()
                    # If neither, check associated q value at position
                    elif next_next_velocity_str in self.value_dict[next_next_position_str]:
                        if next_best_acceleration_str in self.value_dict[next_next_position_str][next_next_velocity_str]:
                            next_q_value = self.value_dict[next_next_position_str][next_next_velocity_str][next_best_acceleration_str]['q_value']
                    # If anything fails, return base reward
                    else: next_q_value = self.value_dict[next_next_position_str]['reward']
                    # Reset racer's metrics
                    racer.reset_p_v(next_position, next_velocity, prev_path, prev_pos)
                # For Q learning, determine next q value based on next state's best action
                else:
                    if next_velocity_str in self.value_dict[next_position_str]:
                        # Check if we have determined best q value of state
                        if 'best_q' in self.value_dict[next_position_str][next_velocity_str]:
                            # Get this value if exists
                            next_q_value = self.value_dict[next_position_str][next_velocity_str]['best_q']
                    # If anything fails, return base reward with visitation penalty
                    else: next_q_value = self.value_dict[next_position_str]['reward'] - self.value_dict[next_position_str]['visit_count']
                # If racer cross finish line, set next_q_value to 100
                if racer.finished():
                    next_q_value = self.get_finish_reward()
                # If the racecar hit a wall, next_q_value = -1000
                elif racer.hit_wall() is not None:
                    next_q_value = self.get_wall_reward()
                    # Reset to closest position on track
                    racer.reset_position(racer.hit_wall(), False)

                """
                Calculate the new q value for state and place within the value dict. Make sure to retrieve previous q value
                (if stored) for delta calculations. 
                """

                # Calculate Q value with below equations
                # SARSA OFF Q = Current Q value + eta * (Reward of next state + discount * Max Next Q - Current Q Value)
                # SARSA ON: Q = Current Q value + eta * (Reward of next state + discount * Next Q value - Curent Q value)
                new_q = current_q + eta * (best_reward + discount * next_q_value - current_q)
                # Build value dict to support new q value
                if current_velocity_str in self.value_dict[current_position_str]:
                    if best_acceleration_str not in self.value_dict[current_position_str][current_velocity_str]:
                        self.value_dict[current_position_str][current_velocity_str][best_acceleration_str] = {}
                else:
                    # Velocity state does not exist so create it within dictionary
                    self.value_dict[current_position_str][current_velocity_str] = {}
                    self.value_dict[current_position_str][current_velocity_str][best_acceleration_str] = {}
                # Check if we have previous q value
                if 'q_value' in self.value_dict[current_position_str][current_velocity_str][best_acceleration_str]:
                    # Store previous q value for delta calculations
                    previous_q = self.value_dict[current_position_str][current_velocity_str][best_acceleration_str]['q_value']
                # Else just set it to the base value
                else:
                    previous_q = self.value_dict[current_position_str]['reward']
                # Assign new q value
                self.value_dict[current_position_str][current_velocity_str][best_acceleration_str]['q_value'] = new_q
                # Update best q value of state if applicable
                if 'best_q' in self.value_dict[current_position_str][current_velocity_str]:
                    if new_q > self.value_dict[current_position_str][current_velocity_str]['best_q']:
                        self.value_dict[current_position_str][current_velocity_str]['best_q'] = new_q
                        # Add acceleration as well
                        self.value_dict[current_position_str][current_velocity_str]['best_acceleration'] = best_acceleration
                else:
                    # If no best_q is selected, this is best_q
                    self.value_dict[current_position_str][current_velocity_str]['best_q'] = new_q
                    # Add acceleration as well
                    self.value_dict[current_position_str][current_velocity_str]['best_acceleration'] = best_acceleration
                
                """
                Calculate delta value
                """

                # Calculate maximum delta of episode
                delta = abs(previous_q - new_q)
                if delta > biggest_delta: 
                    biggest_delta = delta
            
            # For each episode, make sure to decay exploration rate
            exploration_rate *= 0.9999
        # Return the episode count
        return episode_count

    """
    Test the model with a passed in race car. Have the racer start at the starting line and iterate through each 
    position and find the respective best acceleration--with respect to the best q value at each velocity--and
    navigate the track until the finish line is hit. Reset the racer if any walls are hit and store metrics of
    walls hit and moves expended. Make sure to also have a small exploration value to avoid any stuck positions. 
    """
    # Test the model with a passed in race car
    def test(self, racer: Racecar, restart: bool, explore_rate: float) -> None:
        # Keep iterating through the track until finish line
        while racer.finished() == False:
            # Get current position and velocity
            current_position_str = convert_list_to_coordinate(racer.get_position())
            current_velocity_str = convert_list_to_coordinate(racer.get_velocity())
            # Determine what the best action to take at position and velocity
            # Or explore
            if weighted_random([explore_rate, 1-explore_rate]):
                best_acceleration = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
            else: 
                # Fail safe to random if anything goes wrong
                if current_velocity_str not in self.value_dict[current_position_str]: 
                    best_acceleration = [random.choice([-1, 0, 1]), random.choice([-1, 0, 1])]
                else:
                    best_acceleration = self.value_dict[current_position_str][current_velocity_str]['best_acceleration']
            # Traverse racecar with respective restarting conditions
            print_racer_on_track(self.track.track_list, racer.get_position())
            racer.traverse(best_acceleration, restart)