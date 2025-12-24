from track import Track
from typing import List
from calculations import weighted_random, add, get_line_vector

"""
This class defines the Racecar object which contains the position, velocity and acceleration of the Racecar
on a track. The Racecar can technically only be altered via modification of it's acceleration. However, 
during testing, other values are alterable. 
"""

class Racecar:
    def __init__(self, track: Track):
        # Assign a track to the Racecar
        self.track = track
        # Assign start position based on start on track
        self.position = self.track.pick_start_position()
        # Initialize velocity to 0
        self.velocity = [0, 0]
        # Initialize acceleration to 0
        self.acceleration = [0, 0]
        # Create a previous location variable for line drawing
        self.previous_position = [0, 0]
        # Create a line vector for previous path
        self.previous_path = []
        # Create counter for walls hit 
        self.wall_hit = 0
        # Create counter for number of moves
        self.moves = 0

    """
    Getters
    """
    def get_position(self) -> List:
        # Return the current position if no previous path
        if len(self.previous_path) == 0:
            return self.position
        # Return last coordinate of previous path to make sure all ending positions are within track
        return self.previous_path[len(self.previous_path) - 1]
    
    def get_velocity(self) -> List:
        return self.velocity
    
    def get_acceleration (self) -> List:
        return self.acceleration
    
    def get_wall_hit_count(self) -> int:
        return self.wall_hit

    def get_moves(self) -> int: 
        return self.moves
    
    """
    Setters
    """
    def set_position(self, position: List) -> None:
        self.position = position
        # Reset previous path 
        self.previous_path = []

    def set_velocity(self, velocity: List) -> None:
        self.velocity = velocity

    def set_acceleration(self, acceleration: List) -> None:
        self.acceleration = acceleration
    
    def set_previous_position(self, prev_position: List) -> None:
        self.previous_position = prev_position

    """
    Check the validity of Acceleration and return boolean
    """
    def valid_acceleration(self, acceleration: List) -> bool:
        # Both x, y of acceleration must be contained within {-1, 0, 1}
        for element in acceleration:
            if not (element == -1 or element == 0 or element == 1):
                return False
        return True
    
    """
    The maximum velocity magnitude the racer may have is [5, 5]. If the supplied velocity
    exceed this amount, default to the cap. 
    """
    def cap_velocity(self) -> None:
        # Enforce caps on velocity 
        if self.velocity[0] > 5:
            self.velocity[0] = 5
        elif self.velocity[0] < -5:
            self.velocity[0] = -5
        if self.velocity[1] > 5:
            self.velocity[1] = 5
        elif self.velocity[1] < -5:
            self.velocity[1] = -5

    """
    Acceleration function which takes the possibility of a failed acceleration into account. 
    If acceleration is valid, update acceleration member variable. Do not touch other member variables. 
    Debug mode possible. 
    """
    def update_acceleration (self, direction: List, debug = False) -> None:
        # First determine if we follow order at all or not
        acceleration_success = weighted_random([0.8, 0.2])
        if acceleration_success:
            # Determine if is acceleration is valid
            if self.valid_acceleration(direction):
                # Set acceleration
                self.acceleration = direction
                if debug: print(f"Acceleration is now {self.acceleration}")
            else: 
                if debug: print("Invalid Acceleration Command")
        else:
            if debug: print("Acceleration Failed")

    """
    Velocity function that updates the velocity of the Racecar based on the current acceleration
    member variable. Capping the velocity is also checked. 
    Debug mode possible. 
    """
    def update_velocity(self, debug = False) -> None:
        # Update the velocity
        # Add the current acceleration to the velocity
        self.velocity = add(self.velocity, self.acceleration)
        # Cap velocity
        self.cap_velocity()
        if debug: print(f"Velocity is now {self.velocity}")

    """
    Position function that updates the position of the Racecar based on the current velocity member 
    variable. The previous position is updated and a line vector is created and stored within the 
    member variable. 
    Debug mode possible. 
    """
    def update_position (self, debug = False) -> None: 
        # Update the position
        # Save current position
        self.previous_position = self.position
        # Add velocity to position
        self.position = add(self.position, self.velocity)
        # Draw a line vector between previous and current position
        self.previous_path = get_line_vector(self.previous_position, self.position, self.track.track_list)
        if debug: print(self.previous_path)
        if debug: print(f"Position is now {self.position}")
    
    """
    This method alters the Racecar's position and velocity to a custom position and velocity that is 
    passed as a parameter. 
    """
    def reset_p_v (self, position: List, velocity: List, prev_path: List, previous_position: List) -> None:
        self.set_position(position)
        self.set_velocity(velocity)
        self.previous_path = prev_path
        self.previous_position = previous_position

    """
    This method alters the Racecar's position to a custom position that is passed as a parameter. The
    acceleration and velocity member variables are reset to [0, 0]
    """
    def reset_position(self, position: List, restart: bool) -> None:
        # Set the position
        if restart: 
            self.set_position(self.track.pick_start_position())
        else: 
            self.set_position(position)
        # Reset velocity to (0, 0)
        self.set_velocity([0, 0])
        # Reset accelerationm to (0, 0)
        self.set_acceleration([0, 0])

    """
    This method determines Racecar hit a wall. This is done by passing in the previous move as a line vector
    stored wtihin previous_path member variable to the track's closest_wall_on_collision method. If this 
    method returns a valid coordinate, this is the coordinate that we shall reset our Racecar to--as this was
    the Racecar's final valid position before hitting the wall. If no position is returned, we assume our 
    Racecar did not collide with a wall and can continue moving. Metrics are updated and the reset location is 
    returned. Debug mode possible. 
    """
    def hit_wall (self, debug = False) -> None:
        # Pass in line vector to see if we hit a wall
        reset_location = self.track.closest_wall_on_collision(self.previous_path)
        # If reset_location is None, we are clear. Return None
        if reset_location is None:
            return reset_location
        # We hit a wall. Return the reset location
        if debug: print(f"Wall hit. Reset location saved as {reset_location}")
        self.wall_hit += 1
        return reset_location
    
    """
    This method checks if our Racecar touched the finish line. This is done by passing in the previous path's
    line vector into the track's finished method and return that boolean value. There is an edge case where the 
    racer may cross the finish and then hit a wall and then respawn at the finish line so make sure to check 
    the Racecar's current position as well. 
    """
    def finished (self) -> bool:
        # Edge case of crashing and respawning at finish line. 
        # Check previous path if exist
        if len(self.previous_path) > 0:
            return self.track.finished(self.previous_path)
        # If no previous path, check if current position is finish line.
        return self.track.check_finish(self.position)

    """
    Test the Racecar by assigning a custom position, velocity and acceleration and determine if we either cross
    the finish line or hit a wall or remained on the track. Return either 'finish', 'wall', or the final position 
    and final velocity respectively. Acceleration failure chance is not accounted for. 
    """
    # Place racecar at a particular position and return string on where it ends up 
    def psuedo_run(self, position: List, velocity: List, acceleration: List) -> List:
        # Set position 
        self.set_position(position)
        # Set Acceleration
        self.set_acceleration(acceleration)
        # Set Velocity
        self.set_velocity(velocity)
        # Update velocity
        self.update_velocity()
        # Update Position
        self.update_position()
        # Determine if we hit finish line
        if self.finished():
            return "finish"
        # Determine if we hit a wall
        if self.hit_wall():
            return "wall"
        # Still on the road. Return position and velocity of ending location
        return self.get_position(), self.get_velocity()

    """
    Main method to run the Racecar through the track. Pass in an acceleration and factor in the chance of acceleration 
    failure and updatre velocity and position respective. If the Racecar hits the wall, reset position. Make sure to update
    the moves every time. If we cross the finish line, return. 
    """
    def traverse(self, acceleration: List, restart: bool) -> None:
        # This method shifts the acceleration of the racecar and in turn shifts the rest of parameters
        # Update acceleration
        self.update_acceleration(acceleration)
        # Update velocity
        self.update_velocity()
        # Update position
        self.update_position()
        self.moves += 1
        # Check if we finished
        if self.finished():
            return
        # Check if we hit a wall
        reset_position = self.hit_wall()
        # If we hit a wall, reset to appropriate location
        if reset_position is not None: 
            self.reset_position(reset_position, restart)
        # Finished traversing and reset if necessary
    
    