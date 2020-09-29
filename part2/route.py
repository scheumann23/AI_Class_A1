#!/usr/local/bin/python3
# route.py : Calculates the best route for a road trip!
#
# Code by: Vishal Bhalla vibhalla, Neelan Scheumann nscheuma, Cody Harris harrcody
#
# Based on skeleton code by D. Crandall, September 2020
# Adapted from solution for Assignment 1, Part 1
#
from queue import PriorityQueue
import sys

# return a list of possible successor states
def successors(state):
    return [ (shift_row(state, row, dir)) for dir in (-1,1) for row in range(0, ROWS) ] + \
        [ (shift_col(state, col, dir)) for dir in (-1,1) for col in range(0, COLS) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) 

# The solver! - using A*
def solve(initial_board):
    fringe = PriorityQueue()
    fringe.put( (0, (initial_board, [])) )
    while not fringe.empty():
        priority, data = fringe.get()
        state, route_so_far = data
        if state not in visited:
            visited.append(state)
            for (succ, move) in successors( state ):
                if is_goal(succ):
                    return( route_so_far + [move,] )
                    # This is where we can try out different heuristics
                fringe.put((len(route_so_far) + 1 + manhattan(succ), (succ, route_so_far + [move,])))
                #print(succ,(len(route_so_far) + 1 ),manhattan(succ),[move,])
    return False


if __name__ == "__main__":

    start_state = []
    visited = []

    print("Solving...")
    route = solve(tuple(start_state))
    
    #Output [total-segments] [total-miles] [total-hours]  \
    #[total-expected-accidents] [start-city] [city-1] [city-2] ... [end-city]
    
