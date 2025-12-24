from typing import List
import random

"""
This object contains all of the member variables for any track. It converts a text file into 
a List while excluding the coordinates and retaining the row, col integrity. There are also member
methods that determine if certain locations are walls, finish lines or empty. 
"""

class Track:
    def __init__ (self, directory: str, track_name: str) -> None:
        # Pull the track into a 2D array
        self.track_list = self.convert_txt_to_array(f"{directory}/{track_name}.txt")

    """
    Convert the test file into a 2D list while exluding the dimensions line. Make sure to skip
    last element of each line as it is a new line character (\n)
    """
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
            # Append all except llast chracter (new line character)
            for col in range(len(lines[row]) - 1):
                line_list.append(lines[row][col])
            track_list.append(line_list)
        return track_list

    """
    Determine if a particular coordinate is a wall
    """
    def check_wall (self, position: List) -> bool:
        # Check if a particular index is a wall (#)
        return self.track_list[position[0]][position[1]] == "#"

    """
    Determine if a particular coordiante is a Finish point
    """
    def check_finish (self, position: List) -> bool:
        # Check if a particular index is a finish (F)
        return self.track_list[position[0]][position[1]] == "F"
    

    """
    Look through the entier track 2D list and find all start positions. There are usually multiple
    start positions per track so we need a list of all the start positions. 
    """
    def get_start_positions(self) -> List:
        # Return a list of all the start positions on the track
        start_positions = []
        # Go through all elements and return indices that are labeled as 'S'
        for row in range(len(self.track_list)):
            for col in range(len(self.track_list[row])):
                if self.track_list[row][col] == "S":
                    # Insert indices as tuples
                    start_positions.append((row, col))
        return start_positions
    
    """
    Select a random start position on the track. This is done by calling the get_start_positions 
    helper method. 
    """
    def pick_start_position(self) -> List:
        # Get all start positions on the track
        start_positions = self.get_start_positions()
        # Pick a random one from these
        return random.choice (start_positions)

    """
    Given a line vector with the assumption that earlier coordinates correlate to chronologically 
    earlier positions, return the latest position that is not a wall. Meaning, return the last 
    position that is still a road. This will be the position that a Racecar will reset itself to 
    if it collides with a wall.  
    """
    def closest_wall_on_collision(self, line: List) -> List:
        # Iterate through each element and check if it is a wall
        for i in range(len(line)):
            if self.check_wall(line[i]): 
                # If we hit a wall, return the last valid position 
                return line[i - 1]
        # If we didn't hit a wall, return None
        return None

    """
    Given a line vector, check if this line vector intersects any finish points.
    """
    # Determine if we hit a finish line
    def finished(self, line: List) -> bool:
        # Iterate through each element and check if it is finish line
        for i in range(len(line)):
            if self.check_finish(line[i]):
                return True
        return False
