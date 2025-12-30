from typing import List
import sys
import time


"""
Pack track with all positions translated with indiation of where racer is. 
"""
def pack_racer_on_track (track: List, racer_position: List) -> List:
    # Iterate through each track position
    items_on_track = []
    for row in range(len(track)):
        # Store items in row of track
        row_items = ""
        for col in range(len(track[row])):
            if racer_position == [row, col]: 
                # Print a O for the racer
                row_items += "O"
            else:
                # Append whatever is on the track
                row_items += track[row][col]
        items_on_track.append(row_items)
    return items_on_track


"""
Pretty print the entire track and marks the location of the racer within the iteration.
"""
def print_racer_on_track(track: List, racer_position: List) -> None:
    all_rows = ""
    packed_rows = pack_racer_on_track(track, racer_position)
    for row in packed_rows:
        all_rows += row + "\n"
    # Clear terminal
    sys.stdout.flush()
    print(all_rows)
