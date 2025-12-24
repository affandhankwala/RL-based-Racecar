from typing import List
import numpy as np
import random

# Pick either T/F randomly with respect to passed in weights
def weighted_random(weights: List) -> bool:
    # Return T/F dependent on weights
    return random.choices([True, False], weights=weights)[0]

# Add two lists
def add (l1: List, l2: List) -> List:
    # Only add if both are equal length
    if len(l1) != len(l2): return None
    # Add Lists element by element
    return [l1_e + l2_e for l1_e, l2_e in zip(l1, l2)]

# Subtract two lists
def sub (l1: List, l2: List) -> List:
    # Only add if both are equal length
    if len(l1) != len(l2): return None
    # Add Lists element by element
    return [l1_e - l2_e for l1_e, l2_e in zip(l1, l2)]

# Get the top left of any two positions
def get_top_left(left: List, right: List) -> List:
    # Check if left is bottom or top
    if left[0] <= right[0]:
        # left is top left. Return it
        return left
    # Left is bottom left.
    # Top left must have row coordinate of right position and col coordinate of left position
    top_left = [right[0], left[1]]
    return top_left

# Reset positions with respect to one another
def reset_with_respect_top_left (top_left: List, left: List, right: List) -> List:
    # Alter both positions to be relative distances from top_left
    augmented_left = sub(left, top_left)
    augmented_right = sub(right, top_left)
    return augmented_left, augmented_right

# Augment Positions relaative to one another
def augment_positions(position1: List, position2: List) -> List:
    # Augment means to alter the positions so that one of them is [0, 0] while other is 
    # the same distance away.
    # Determine which position is more left
    if position1[1] < position2[1]: 
        # Position1 is left position. 
        # Get top left position
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

# Get direction for line from origin to goal
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

# Return a list of indices indicating straight line from origin to goal
def draw_straight_line(corner_origin: List, corner_goal: List) -> List:
    # Get direct line between two points:
    # Initialize straight_line list
    straight_line_indices = [corner_origin]
    current_location = corner_origin
    # Iterate till we reach the goal
    while current_location != corner_goal:
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

# Revert augmentation of list with respect to top left
def revert_augment(l: List, top_left: List) -> List:
    # Add coordinates of top_left to each coordinate in l
    new_l = []
    for coordinate in l:
        new_l.append(add(coordinate, top_left))
    return new_l

# Draw Line Vector between two points
def get_line_vector(previous: List, current: List):
    # Determine the quickest path from position1 to position 2
    # Augment the two positions 
    previous_augmented, current_augmented, top_left = augment_positions(previous, current)
    # Starting from either corner, get straight line through points
    line_indices_augmented = draw_straight_line(previous_augmented, current_augmented)
    # Revert indices augmentation and return
    return revert_augment(line_indices_augmented, top_left)
