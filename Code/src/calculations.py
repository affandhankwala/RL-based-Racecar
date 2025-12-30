from typing import List, Dict
import numpy as np
import random


"""
This file is responsible for any calculation that our model needs to compute that is not
specifically tied to any class and is utilzied multiple times.
"""

"""
Pick either T/F randomly with respect to passed in weights. 
Weights parameter can hold a maximum of two float values that contain the proportions
of each choice. Return the selected boolean with respect to proportions.
"""
def weighted_random(weights: List) -> bool:
    # Return T/F dependent on weights
    return random.choices([True, False], weights=weights)[0]

"""
Add the two parameterized lists and return a third list comprised of the sums of both list's
respective indices. 
"""
def add (l1: List, l2: List) -> List:
    # Only add if both are equal length
    if len(l1) != len(l2): return None
    # Add Lists element by element
    return [l1_e + l2_e for l1_e, l2_e in zip(l1, l2)]

"""
Subtract two lists from one another. The second parameterized list is subtracted from the 
first parameterized list. A third list is returned containing the subtracted values. 
"""
def sub (l1: List, l2: List) -> List:
    # Only add if both are equal length
    if len(l1) != len(l2): return None
    # Subtract Lists element by element
    return [l1_e - l2_e for l1_e, l2_e in zip(l1, l2)]

"""
Given two [x,y] coordinates, imagine a 2D rectangle with both points at any corner.
This method determines the coordinates for the top left corner of imaginary rectange.
"""
def get_top_left(left: List, right: List) -> List:
    # Left is coordinate that is closer to the left (West) 
    # Check if left is bottom or top corner
    # Check left coordinate's row is < or equal to right coordinate's row value
    if left[0] <= right[0]:
        # left is top left. Return it
        return left
    # Left is bottom left.
    # Top left must have row coordinate of right position and col coordinate of left position
    top_left = [right[0], left[1]]
    return top_left

"""
Set top left to [0,0] and alter both coordinates with respect to distance from this anchor.
"""
def reset_with_respect_top_left (top_left: List, left: List, right: List) -> List:
    # Alter both positions to be relative distances from top_left
    augmented_left = sub(left, top_left)
    augmented_right = sub(right, top_left)
    return augmented_left, augmented_right

"""
Augment two coordinates with respect to one another. This means to set one of the coordinates
to [0, 0] and modify the other such that their relative distance remains the same. This is 
done by assining the coordinate that is more left (WEST) as the [0, 0] anchor and then 
augmenting the second coordinate with respect to this anchor. 
"""
# Augment Positions relative to one another
def augment_positions(position1: List, position2: List) -> List:
    # Determine which position is more left
    if position1[1] < position2[1]: 
        # Position1 is left position. 
        # Create an imaginary rectangle encompassing both coordinates and determine top left
        # coordinate of this rectangle
        top_left = get_top_left(position1, position2)
        # Augment values with respect to top left
        new_pos1, new_pos2 = reset_with_respect_top_left(top_left, position1, position2)
    else:
        # Position2 is considered left position (Both could be within same column)
        # Get top left position
        top_left = get_top_left(position2, position1)
        # Augment values with respect to top left
        new_pos2, new_pos1 = reset_with_respect_top_left(top_left, position2, position1)
    return new_pos1, new_pos2, top_left

"""
Given two parameterized coordinates representing the start and the goal state, return
a string corresponding to a straight line through the two points. 
"""
def get_direction(origin: List, goal: List) -> str:
    # Get the difference to determine direction of straight line
    difference = sub(origin, goal)
    # If difference is (<0, <0), goal is SE of origin
    if difference[0] < 0 and difference[1] < 0: return "SE"
    # If difference is (<0, 0), goal is S of origin
    if difference[0] < 0 and difference[1] == 0: return "S"
    # If difference is (<0, >0), goal is SW of origin
    if difference[0] < 0 and difference[1] > 0: return "SW"
    # If difference is (0, <0), goal is E
    if difference[0] == 0 and difference[1] < 0: return "E"
    # If difference is (0, 0), goal is equal to origin
    if difference[0] == 0 and difference[1] == 0: return "None"
    # If difference is (0, >0), goal is W
    if difference[0] == 0 and difference[1] > 0: return "W"
    # If difference is (>0, <0), goal is NE
    if difference[0] > 0 and difference[1] < 0: return "NE"
    # If difference is (>0, 0), goal is N
    if difference[0] > 0 and difference[1] == 0: return "N"
    # If difference is (>0, >0), goal is NW 
    if difference[0] > 0 and difference[1] > 0: return "NW"

"""
Given a string direction, determine the movement required to move in that direction. Meaning
if we were to traverse North, we would need to go up one row. This translates to [-1, 0]. 
This is done for all possible directions except None position.
"""
# Create incrementors based on direction
def get_incrementors (direction: str) -> List:
    # If direction == N, increment by [-1, 0]
    if direction == "N": return -1, 0
    # If direction == NE, increment by [-1, 1]
    if direction == "NE": return -1, 1
    # If direction == E, increment by [0, 1]
    if direction == "E": return 0, 1
    # If direction == SE, increment by [1, 1]
    if direction == "SE": return 1, 1
    # If direction == S, increment by [1, 0]
    if direction == "S": return 1, 0
    # If direction == SW, increment by [1, -1]
    if direction == "SW": return 1, -1
    # If direction == W, increment by [0, -1]
    if direction == "W": return 0, -1
    # If direction == NW, increment by [-1, -1]
    if direction == "NW": return -1, -1

"""
Return a list of indices corresponding to as straight line as possible from the origin to 
the goal coordinates. 
"""
def draw_straight_line(corner_origin: List, corner_goal: List) -> List:
    # Initialize straight_line list
    straight_line_indices = [corner_origin]
    # Set the current location as origin
    current_location = corner_origin
    # Iterate till we reach the goal
    while current_location != corner_goal:
        # Determine which direction we need to traverse via get_direction
        direction = get_direction(current_location, corner_goal) 
        # If origin and goal are the exact same, we return either
        if direction == "None": return straight_line_indices
        # Get incrementors for movement in particular direction
        row_incrementor, col_incrementor = get_incrementors(direction)
        # Alter current location
        current_location = add(current_location, [row_incrementor, col_incrementor])
        # Add location to indices
        straight_line_indices.append(current_location)
    return straight_line_indices

"""
Augmented coordinates are those that are 'encapsulated' in an imaginary rectangle and are 
altered to represent their location within the rectangle while maintaining their relative 
distance. This method reverts the alteration to turn both coordintates (within the l List) 
back to their original values. This is done by adding both coordinates with the coordinates
of the top left of the rectangle. 
"""
def revert_augment(l: List, top_left: List) -> List:
    # Add coordinates of top_left to each coordinate in l. This will revert the values
    new_l = []
    for coordinate in l:
        new_l.append(add(coordinate, top_left))
    return new_l

"""
A vector may contain values that are beyond the range of the track. We do not care about these
values as assume them to be invalid/wall. Return only the portion of the list whose coordiantes are
contained within the matrix parameter. 
"""
def refine_line_vector(line_vector: List, matrix: List) -> List:
    # Returns only the portion of the line_vector that is contained within matrix
    # Get matrix dimensions
    row_size = len(matrix)
    col_size = len(matrix[0])
    # Iterate through line_vectors
    valid_coordinates = []
    for coordinate in line_vector:
        row, col = coordinate
        # If any coordinate is invalid, return the valid coordinates
        if row < 0 or row >= row_size or col < 0 or col >= col_size:
             # It is impossible for a straight line to step outside matrix dimensions and then re-enter 
            return valid_coordinates
        # If valid, append
        valid_coordinates.append(coordinate)
    # All valid so just return
    return valid_coordinates

"""
This method draws a line vector between two points. This is done by first drawing out the imaginary
rectangle then drawing the straight lines between the two augmented positions. The coordinates'
augmentation is then reverted and then finally the line vector is refined before returning. 
"""
def get_line_vector(previous: List, current: List, track_list: List) -> List:
    # Determine the quickest path from position1 to position 2
    # Augment the two positions and store top_left for reverting augmentation
    previous_augmented, current_augmented, top_left = augment_positions(previous, current)
    # Starting from either corner, get straight line through points
    line_indices_augmented = draw_straight_line(previous_augmented, current_augmented)
    # Revert indices augmentation and return
    line_indices_reverted = revert_augment(line_indices_augmented, top_left)
    # Refine to get valid line vector
    line_vector = refine_line_vector(line_indices_reverted, track_list)
    return line_vector

"""
This method returns the maximum value within a dictionary while ignoring certain keys. 
This is critical when attempting to determine the maximum value of a subset of keys within
a dictionary. 
"""
def get_max_from_subset(dict: Dict, keys_to_ignore: List) -> str:
    # Initialize maximum values
    max_value = -99999
    max_key = None
    for key, value in dict.items(): 
        # If key is contained within keys_to_ignore, ignore it
        if key in keys_to_ignore:
            continue
        # Compare value with max value
        if value > max_value:
            max_value = value
            max_key = key
    # Return the maximum key in the format it was passed in
    return max_key

"""
This method converts a coordinate in the format str("[x, y]") to list in the format
List(x, y). 
"""
def convert_coordinate_to_list(coordinate: str) -> List:
    # Get the x value
    # Exclude [ character
    x_portion = int(coordinate[1:].split(',')[0])
    # Get y value
    # Exclude ] character
    y_portion = int(coordinate.split(',')[1][:-1])
    return [x_portion, y_portion]

"""
This method converts a List in the format List(x, y) to a coordinate in the format 
str("[x, y]").
"""
def convert_list_to_coordinate(l: List) -> str:
    return f"[{l[0]}, {l[1]}]"

"""
Calculate and return mean of a list.
"""
def list_mean(l: List) -> float:
    return sum(l) / len(l)