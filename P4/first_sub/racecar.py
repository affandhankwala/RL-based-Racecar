from track import Track
from typing import List
from calculations import weighted_random, add, get_line_vector
import random

class Racecar:
    def __init__(self, track: Track):
        # Assign a track off the start
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

    # Getters
    def get_position(self) -> List:
        return self.position
    
    def get_velocity(self) -> List:
        return self.velocity
    
    def get_acceleration (self) -> List:
        return self.acceleration
    
    # Setters
    def set_position(self, position: List) -> None:
        self.position = position

    def set_velocity(self, velocity: List) -> None:
        self.velocity = velocity

    def set_acceleration(self, acceleration: List) -> None:
        self.acceleration = acceleration
    
    # Reset the position to one of valid start positions of track
    def reset_position(self) -> None:
        self.position = self.track.pick_start_position()

    # Check Validity of Acceleration
    def valid_acceleration(self, acceleration: List) -> bool:
        # Both x, y of acceleration must be contained within {-1, 0, 1}
        for element in acceleration:
            if not (element == -1 or element == 0 or element == 1):
                return False
        return True
    
    # Cap Velocity if needed
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

    # Accelerate function
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

    # Velocity function
    def update_velocity(self, debug = False) -> None:
        # Update the velocity
        # Add the current acceleration to the velocity
        self.velocity = add(self.velocity, self.acceleration)
        # Cap velocity
        self.cap_velocity()
        if debug: print(f"Velocity is now {self.velocity}")

    # Position Function
    def update_position (self, debug = False) -> None: 
        # Update the position
        # Save current position
        self.previous_position = self.position
        # Add velocity to position
        self.position = add(self.position, self.velocity)
        if debug: print(f"Position is now {self.position}")

    # Check if collide with wall
    def hit_wall (self, debug = False) -> None:
        # Draw a line vector between previous and current position
        self.previous_path = get_line_vector(self.previous_position, self.position)
        if debug: print(self.previous_path)
        # Pass in line vector to see if we hit a wall
        reset_location = self.track.closest_wall_on_collision(self.previous_path)
        # If reset_location is None, we are clear otherwise we hit wall
        if reset_location is None:
            return False
        if debug: print(f"Wall hit. Resetting to {reset_location}")
        return True

    def move(self) -> None:
        # This method controls movement of car
        return
    
    