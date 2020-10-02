#!/usr/local/bin/python3
# route.py : Calculates the best route for a road trip!
#
# Code by: Vishal Bhalla vibhalla, Neelan Scheumann nscheuma, Cody Harris harrcody
#
# Based on skeleton code by D. Crandall, September 2020
# Adapted from solution for Assignment 1, Part 1

from queue import PriorityQueue
import sys
from math import sin, cos, sqrt, atan2, radians
import time

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
    
# chooses the hueristic based on input parameters
def hueristic(start, end, route, cost_func):
    if cost_func == 'segments':
        return segments_cost(route) / max_segment_length
    elif cost_func == 'distance':
        return get_distance_apart(start, end)
    elif cost_func =='time':
        return get_distance_apart(start, end) / max_speed
    elif cost_func == 'cycling':
        return get_distance_apart(start, end) * 0.000001 * max_speed

#loads edge data
def load_data(file_name):
    data_list = []
    with open(file_name, 'r') as file:
        for line in file:
            data_list.append(tuple(line.split()))
    return data_list

def city_list():
    return set([city[0] for city in road_segs] + [city[1] for city in road_segs])
  
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
def get_shortest_leg(state):
    match_first = [city[2] for city in road_segs if city[0] in state]
    match_second = [city[2] for city in road_segs if city[1] in state]
    return float(min(match_first + match_second))

def get_distance_apart(start, end):
    if start in cities_have_gps and end in cities_have_gps:
        start_lat_long = [coords for coords in gps_data if coords[0] in start]
        start_lat = float(start_lat_long[0][1])
        start_long = float(start_lat_long[0][2])
        end_lat_long = [coords for coords in gps_data if coords[0] in end]
        end_lat = float(end_lat_long[0][1])
        end_long = float(end_lat_long[0][2])
        sp_dist = spherical_dist_calc(start_lat, start_long, end_lat, end_long) - 5
        if sp_dist > max_segment_length:
            return shortest_dist
        else:
            return sp_dist
    else:
        return shortest_dist

# distance between two points, using long/lat
# Retrived this code from the following link
# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
def spherical_dist_calc(lat1, lon1, lat2, lon2):
    R = 3956
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
    match_first = [tuple(city[1:4]) for city in road_segs if city[0] == state]
    match_second = [tuple([city[0], city[2], city[3]]) for city in road_segs if city[1] == state]
    return match_first + match_second

# check if we've reached the goal
def is_goal(current_city, end_city):
    return current_city == end_city 

# The solver! - using A*
def solve(route_params):
    fringe = PriorityQueue()
    #Fringe is (priority, (current city, route, cost))
    curr_city = route_params[0]
    end_city = route_params[1]
    cost_function = route_params[2]
    fringe.put((0, (curr_city, [curr_city], 0)))
    visited = []  
    while not fringe.empty():
        priority, data = fringe.get()
        curr_city, route_so_far, cost = data
        if is_goal(curr_city, end_city):
                return route_so_far
        if curr_city not in visited:
            visited.append(curr_city)
            for succ in successors(curr_city):
                cost_so_far = calc_cost([curr_city, succ[0]], cost_function) + cost
                fringe.put((cost_so_far + hueristic(succ[0], end_city, route_so_far + [succ[0]], cost_function), (succ[0], route_so_far + [succ[0]], cost_so_far)))
                #fringe.put((cost_so_far, (succ[0], route_so_far + [succ[0]], cost_so_far)))
        return False


if __name__ == "__main__":
    t0 = time.time()
    if(len(sys.argv) != 4):
        raise(Exception("Error: Expected start city, end city, and cost function. No Spaces in Arguments!"))
        
    if(sys.argv[3] not in ['segments', 'distance', 'time', 'cycling', 'statetour']):
        raise(Exception("Error: Cost function should be one of: segments, distance, time, cycling, statetour"))
        
    start_state = tuple(sys.argv[1:])  
    
    #Preprocess data
    road_segs = load_data('road-segments.txt')
    gps_data = load_data('city-gps.txt')
    cities = city_list()
    if sys.argv[1] not in cities:
        raise(Exception('Error: \'{}\' not in list of road segments'.format(sys.argv[1])))
    if sys.argv[2] not in cities:
        raise(Exception('Error: \'{}\' not in list of road segments'.format(sys.argv[2])))
    #Get list of cities in gps_data for faster processing
    cities_have_gps = [city[0] for city in gps_data]
    #Get the shortest road coming from destination city
    shortest_dist = get_shortest_leg(sys.argv[2])
    seg_lengths = [int(road_data[2]) for road_data in road_segs]
    seg_lengths.sort()
    max_segment_length = seg_lengths[-1]
    speeds = [int(road_data[3]) for road_data in road_segs]
    speeds.sort()
    max_speed = speeds[-1]
    print("Solving...")
    route = solve(tuple(start_state))
    if route:
        print(segments_cost(route), distance_cost(route), time_cost(route), cycling_cost(route), ' ', end='')
        for city in route:
            print(city, ' ', end = '')
    else:
        print("No viable route between start and end cities")

    print('\n', time.time()-t0)
