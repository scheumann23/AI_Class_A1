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

# chooses which cost function to use
def calc_cost(route, cost_func):
    if cost_func == 'segments':
        return segments_cost(route)
    elif cost_func == 'distance':
        return distance_cost(route)
    elif cost_func =='time':
        return time_cost(route)
    elif cost_func == 'cycling':
        return cycling_cost(route)

#loads edge data
def load_data(file_name):
    data_list = []
    with open(file_name, 'r') as file:
        for line in file:
            data_list.append(tuple(line.split()))
    return data_list
  
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
def successors(state, edge):
    match_first = [city[1:4] for city in road if city[0] in state]
    match_second = [tuple([city[0], city[2], city[3]]) for city in road if city[1] in state]
    return match_first + match_second

# check if we've reached the goal
def is_goal(state, end_city):
    return state[1][0] == end_city 

# The solver! - using A*
def solve(route_params):
    fringe = PriorityQueue()
    #Fringe is (priority, (current city, route, cost))
    fringe.put((0, (route_params[0], [], 0)))
    visited = []
    road_segs = load_data('road-segments.txt')
    gps = load_data('city-gps.txt')
    
    while not fringe.empty():
        priority, data = fringe.get()
        state, route_so_far, cost = data
        if state not in visited:
            visited.append(state)
            for succ in successors(state, road_segs):
                if is_goal(succ, route_params[1]):
                    return(route_so_far.append(succ))
                    # This is where we can try out different heuristics
                route_so_far = route_so_far.append(succ)
                cost_so_far = calc_cost(route_so_far, route_params[2])
                fringe.put((cost_so_far + euclid_dist(succ), (succ, route_so_far, cost_so_far)))
                
    return False


if __name__ == "__main__":
    if(len(sys.argv) != 4):
        raise(Exception("Error: Expected start city, end city, and cost function. No Spaces in Arguments!"))
        
    if(sys.argv[3] not in ['segments', 'distance', 'time', 'cycling', 'statetour']):
        raise(Exception("Error: Cost function should be one of: segments, distance, time, cycling, statetour"))
        
    start_state = tuple(sys.argv[1:])   

    print("Solving...")
    route = solve(tuple(start_state))
    
    #Output [total-segments] [total-miles] [total-hours]  \
    #[total-expected-accidents] [start-city] [city-1] [city-2] ... [end-city]
    print(route)
