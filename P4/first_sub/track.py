from typing import List
import random

class Track:
    def __init__ (self, directory: str, track_name: str) -> None:
        # Pull the track into a 2D array
        self.track_list = self.convert_txt_to_array(f"{directory}/{track_name}.txt")

    def convert_txt_to_array(self, file_path: str) -> List:
        # Read all values within track file
        with open(file_path, "r") as file:
            # Read all the lines within the notepad
            lines = file.readlines()
        # Process the lines
        # Iterate through all lines and translate that character to a 2D List
        track_list = []
        # Skip the dimensions line
        for row in range(1, len(lines)):
            line_list = []
            for col in range(len(lines[row])):
                line_list.append(lines[row][col])
            track_list.append(line_list)
        return track_list

    def check_wall (self, position: List) -> bool:
        # Check if a particular index is a wall (#)
        return self.track_list[position[0]][position[1]] == "#"

    def get_start_positions(self) -> List:
        # Return a list of all the start positions on the track
        start_positions = []
        # Go through all elements and return indices that are labeled as 'S'
        for row in range(len(self.track_list)):
            for col in range(len(self.track_list[row])):
                if self.track_list[row][col] == 'S':
                    # Insert indices as tuples
                    start_positions.append((row, col))
        return start_positions
    
    def pick_start_position(self) -> List:
        # Get all start positions on the track
        start_positions = self.get_start_positions()
        # Pick a random one from these
        return random.choice (start_positions)

    # Return closest road if position line hits wall
    def closest_wall_on_collision(self, line: List) -> List:
        # Iterate through each element and check if it is a wall
        for i in range(len(line)):
            if self.check_wall(line[i]): 
                # If we hit a wall, return the last valid position 
                return line[i - 1]
        # If we didn't hit a wall, return None
        return None
