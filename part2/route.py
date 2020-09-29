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

#segments cost function
def segments_cost():
    return

# distance cost function
def distance_cost():
    return

# time cost function
def time_cost():
    return

# cycling cost function
def cycling_cost():
    return

# graph preprocessing for missing cities in long/lat
def missing_cities():
    return

# distance between two points, using long/lat
def euclid_dist():
    return

# return a list of possible successor states
def successors(state):
    return [ (shift_row(state, row, dir)) for dir in (-1,1) for row in range(0, ROWS) ] + \
        [ (shift_col(state, col, dir)) for dir in (-1,1) for col in range(0, COLS) ]

# check if we've reached the goal
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) 

# The solver! - using A*
def solve(route_params):
    fringe = PriorityQueue()
    #Fringe is (priority, (current city, list of steps, cost))
    fringe.put((0, (route_params[0], [], 0)))
    visited = []
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
    if(len(sys.argv) != 4):
        raise(Exception("Error: expected start city, end city, and cost function. No Spaces in Arguments!"))
        
    start_state = tuple(sys.argv[1:])   

    print("Solving...")
    route = solve(tuple(start_state))
    
    #Output [total-segments] [total-miles] [total-hours]  \
    #[total-expected-accidents] [start-city] [city-1] [city-2] ... [end-city]
    print(route)
