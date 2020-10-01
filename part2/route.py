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
from math import sin, cos, sqrt, atan2, radians

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
def segments_cost(route):
    return (len(route) - 1)

# distance cost function
def distance_cost(route):

    dist = 0
    if len(route) == 2:
        for i in range(len(road_segs)):
            if road_segs[i][0] == route[0] and road_segs[i][1] == route[1] or (road_segs[i][0] == route[1] and road_segs[i][1] == route[0]):
                dist = int(road_segs[i][2])
                exit
        return round(dist,5)
    else:
        for i in range(len(road_segs)):
            if road_segs[i][0] == route[0] and road_segs[i][1] == route[1] or (road_segs[i][0] == route[1] and road_segs[i][1] == route[0]):
                dist = int(road_segs[i][2])
                exit
        return round(dist  + distance_cost(route[1:]),5)

# time cost function
def time_cost(route):
    dist = 0
    speed = 0
    if len(route) == 2:
        for i in range(len(road_segs)):
            if road_segs[i][0] == route[0] and road_segs[i][1] == route[1] or (road_segs[i][0] == route[1] and road_segs[i][1] == route[0]):
                dist = int(road_segs[i][2])
                speed = int(road_segs[i][3]) + 5
                exit
        return round(dist / speed, 5)
    else:
        for i in range(len(road_segs)):
            if road_segs[i][0] == route[0] and road_segs[i][1] == route[1] or (road_segs[i][0] == route[1] and road_segs[i][1] == route[0]):
                dist = int(road_segs[i][2])
                speed = int(road_segs[i][3]) + 5
                exit
        return round(dist / speed + time_cost(route[1:]),5)

# cycling cost function
def cycling_cost(route):
    dist = 0
    speed = 0
    if len(route) == 2:
        for i in range(len(road_segs)):
            if (road_segs[i][0] == route[0] and road_segs[i][1] == route[1]) or (road_segs[i][0] == route[1] and road_segs[i][1] == route[0]):
                dist = int(road_segs[i][2])
                speed = int(road_segs[i][3])
                exit
        return round(speed * 0.000001 * dist, 5)
    else:
        for i in range(len(road_segs)):
            if road_segs[i][0] == route[0] and road_segs[i][1] == route[1] or (road_segs[i][0] == route[1] and road_segs[i][1] == route[0]):
                dist = int(road_segs[i][2])
                speed = int(road_segs[i][3])
                exit
        return round(speed * 0.000001 * dist + cycling_cost(route[1:]),5)

# graph preprocessing for missing cities in long/lat
def missing_cities():
    return

def get_distance_apart(start, end):
    if start in cities_have_gps and end in cities_have_gps:
        start_lat_long = [coords for coords in gps_data if coords[0] in start]
        start_lat = float(start_lat_long[0][1])
        start_long = float(start_lat_long[0][2])
        end_lat_long = [coords for coords in gps_data if coords[0] in end]
        end_lat = float(end_lat_long[0][1])
        end_long = float(end_lat_long[0][2])
        return spherical_dist_calc(start_lat, start_long, end_lat, end_long)
    else:
        return 0

# distance between two points, using long/lat
# Retrived this code from the following link
# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def spherical_dist_calc(lat1, lon1, lat2, lon2):
    R = 3958.8
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
#End Copy

# return a list of possible successor states
def successors(state):
    match_first = [city[1:4] for city in road_segs if city[0] in state]
    match_second = [tuple([city[0], city[2], city[3]]) for city in road_segs if city[1] in state]
    return match_first + match_second

# check if we've reached the goal
def is_goal(state, end_city):
    return state[0] == end_city 

# The solver! - using A*
def solve(route_params):
    fringe = PriorityQueue()
    #Fringe is (priority, (current city, route, cost))
    fringe.put((0, (route_params[0], [route_params[0]], 0)))
    visited = []  
    while not fringe.empty():
        priority, data = fringe.get()
        state, route_so_far, cost = data
        if state not in visited:
            visited.append(state)
            for succ in successors(state):
                print(succ)
                if is_goal(succ, route_params[1]):
                    return route_so_far + [succ[0]]
                cost_so_far = calc_cost(route_so_far + [succ[0]], route_params[2])
                fringe.put((cost_so_far + get_distance_apart(succ, route_params[1]), (succ, route_so_far + [succ[0]], cost_so_far)))
        print(fringe.get())
                
    return False


if __name__ == "__main__":
    if(len(sys.argv) != 4):
        raise(Exception("Error: Expected start city, end city, and cost function. No Spaces in Arguments!"))
        
    if(sys.argv[3] not in ['segments', 'distance', 'time', 'cycling', 'statetour']):
        raise(Exception("Error: Cost function should be one of: segments, distance, time, cycling, statetour"))
        
    start_state = tuple(sys.argv[1:])   
    road_segs = load_data('road-segments.txt')
    gps_data = load_data('city-gps.txt')
    #Get list of cities in gps_data for faster processing
    cities_have_gps = [city[0] for city in gps_data]
    print("Solving...")
    route = solve(tuple(start_state))
    
    #Output [total-segments] [total-miles] [total-hours]  \
    #[total-expected-accidents] [start-city] [city-1] [city-2] ... [end-city]
    print("end", route)
