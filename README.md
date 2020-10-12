# Part 1: The 2020 Puzzle
The state space for this puzzle solver is a 5*4 board. The allowed moves are for a full row to move 1 step left or right and full column to move 1 step up or down
## Hueristics Evaluated

### Manhattan Distance
The manhattan distance was calculated from the current state to goal state by summing up the absolute different between x and y indexes for the two boards however it was found to be overestimating at times.E.g. in the board below the 2nd can be corrected in 1 move up however the manhattan distance calculated would be 4.
1 17 3 4 5 
10 2 7 8 9
11 6 13 14 15
16 12 18 19 20
### Number out of Order
Number of out of order numbers was another heuristic we tried. This also was overestimating. E.g. In this case too the one move solves the board but there are 4 numbers out of order
1 17 3 4 5 
6 2 8 9 10
11 7 13 14 15
16 12 18 19 20
### Number of inversions
Number of inversions heuristic checks how many neighbors do not have the right neighbor to be greater than itself. This also heuristic also can be shown to overestimate using the same board as above
1 17 3 4 5 
6 2 8 9 10
11 7 13 14 15
16 12 18 19 20

### Number of horizontal and vertical moves
Here we calculate the legal horizontal and vertical moves by summing up the number of vertical distances and horizontal differences  between the current state and goal state and then divide them by number of rows and colums respectively and summing that up. It is a modification of the manhattan distance. This is an admissible heuristic. We tested it for up to 12 board shown below:
12 18 15 14 10
17 8 5 20 2
3 7 13 4 16
11 6 19 9 1

# Part 2: Road trip!

## State Space

The state space of this problem includes all cities or road intersections that can be found in the road-segments.txt file. 

## Sucessor Function

For a given state, the successor function finds all of the cities or road intersections that are directly connected to the current city. Roads are bidirectional, which the successor function handles by looking for the current city name in the road-segments.txt file in either the first or second position, and then returns the other city in that line. 

## Edge Weights

### Distance Edge Weight

This weight is retrieved by using the distance number for each segment in the road-segments.txt file.

### Time Edge Weight

Time edge weight uses the distance egde weight divided by the speed limit found in the road-segments.txt file, plus 5

### Segments Edge Weight

For this edge weight, all edges are weighted the same, and are given a weight of 1.

### Cycling Edge Weight

The cycling edge weight uses the speed for the road segment in road-segments.txt file, multiplied by 0.000001. This weight is then multiplied by the length of the road segment.

## Goal State

The goal state is the destination city supplied by the user. Also the goal state should be accompanied by the route that minimizes the cost function suggested 

## Hueristics

### GPS Distance Only

In the file city-gps.txt, there are many cities GPS locations in lattitude and longitude. This file does not contain all locations for all the end points in road-segments.txt.

The hueristic calculates the distance between the current state, and the goal state. As the locations are in lattitude and longitude, the euclidean distance gives a distance in degrees, that is not very useful when estimating the distance in miles. Also, as we are dealing with two points on a sphere, euclidean distance is not the best estimate. To remedy both of these problems, a calculation can be made to calculate arc length between two points given the radius of the sphere (Earth). The formula for this calculation is called the Haversine formula and is primarily used for navigation [1]. We found a python function that calculates the Haversine distance, which is used in the code [2].

Haversine formula: 

Where:  
<img src="https://render.githubusercontent.com/render/math?math=lat_1, lat_2, long_1, long_2"> are the lattitude and longitude of the start and end points in the calculation.

and

<img src="https://render.githubusercontent.com/render/math?math=latrad_1 = radians(lat_1)">
<img src="https://render.githubusercontent.com/render/math?math=latrad_2 = radians(lat_2)">
<img src="https://render.githubusercontent.com/render/math?math=longrad_1 = radians(lat_1)">
<img src="https://render.githubusercontent.com/render/math?math=longrad_2 = radians(lat_2)">
<img src="https://render.githubusercontent.com/render/math?math=dlat = latgrad_2 - latgrad_1">
<img src="https://render.githubusercontent.com/render/math?math=dlong = longrad_2 - longrad_1">
<img src="https://render.githubusercontent.com/render/math?math=R = radius in miles = 3956">

<img src="https://render.githubusercontent.com/render/math?math=haversine = R * 2*arctan(\frac{(sin(\frac{dlat}{2})^2 + cos(latrad_1) * cos(latrad_2) * sin(\frac{dlon}{2})^2)}{\sqrt{1 - (sin(\frac{dlat}{2})^2 + cos(latrad_1) * cos(latrad_2) * sin(\frac{dlon}{2})^2)}}">

In the case that the current city does not have a GPS coordinate, then the hueristic finds all the road segments attached to the goal city, and uses the minimum segment length.

#### Modifications for various costs

As there are four cost functions, this distance discussed above needs to be adjusted to match the cost function being used. For the distance cost, there are no adjustments. When the cost is the number of segments, the haversine distance is divided by the largest segment length found in the road-segments.txt file. If the cost function is time, then the haversine distance is divided by the fastest speed in the road-segments.txt file plus 5. Lastly, the cycling hueristic uses the haversine distance times 0.000001 times the max possible speed plus 5.

#### Why this hueristic is admissible

With accurate data, this hueristic alone is admissible because this distance would be if there were a strait road between two cities with no turns or elevation changes. This is the shortest distance between two points. If there were turns or elevation changes, then the driving distance would be greater than the computed distance.

If there is no GPS, when using the shortest segment leg attached to the goal city, this is also admissible. The reason this cannot overestimate the cost, is because if the current city is the city right next to the goal city, then the shortest cost can only be the shortest distance connected to the goal. 

#### Why this hueristic still sometimes overestimates

While in theory, the hueristic explained should never overestimate, due to the data given sometimes it overestimates. For example, the GPS coordinate for Lakes District, Washington is actually a coordinate in the state of West Virginia. Due to being across the country from where it is supposed to be, this greatly over estimates the distance. 

Not all of the discrepancies in the data are so greatly exaggerated, but even slight overestimates could result in getting sub-optmial routes. There are many cases where the straight line distance between two cities is larger than the segment of road connecting the two cities. 

#### Adjustments to the Hueristic to make it admissible, and a better estimate, despite the inconsistent data

There is a check to see if any hueristic calculated is longer than the largest segment, then the hueristic uses the shortest segment length connected to the goal city.

After some testing, we also found that multiplying the distance by 0.75 would still allow the distance to be an underestimate, while still getting as close to the true distance as possible.

Lastly, we implemented a second function that averages the lattitudes and longitudes of all of the neighbors of the starting city. Then this averaged GPS coordinate is used to calculated the haversine distance to the goal. This could help in the case in which there is no GPS, then this could try to estimate the location of the current city or interchange. This calculation could be not admissible, to combat this, the hueristic value used is the minimum between this averaged lattitude and longitude and the actual lattitude and longitude.

## Explanation of Search Algorithm

The algoritm is an A* search algorithm, that uses the hueristic that was previously discussed. The fringe used is a priority queue that uses a priority which is the current cost (based on the given cost variable supplied by the user) plus the hueristic. The current state is gained by popping the city in the fringe with the lowest priority calculation.

The fringe includes the current city explored, route so far, and cost so far of the route. When a state is explored for sucessors, it is checked that the sucessors are not in the list of visited states before adding it to the fringe. 

## Discussion of Issues

The implementation of an A* search was not overly difficult, but the difficulties came when realizing that a seemingly admissible hueristic was returning overestimates. As discussed in the section about adjusting the hueristic, we are taking 75% of the distance calculated instead of 100%. We are assuming that this is enough based on many tests, but it is possible that we might have to reduce the distance further to get correct routes.


# Part 3: Choosing Teams

## Description of Search Problem
We decided to use lcoal search to solve this problem. 
### State Space
The state space for this problem is all of the possible pairings of students into groups of either either 1, 2 or 3.
### Initial State
The initial state semi-randomly pairs up each student into a group of three until the final 1, 2, or 3 students who also get paired up. This initial state minimizes the time grading becuase the number of teams is as small as possible.
### Successor function
The successor function returns possible boards with either two students that have had their teams swapped, a person being added to a team of 2, a person being added to a team of 1, or a person being split off from their team to form a new team.

## How the search algorithm works
After choosing the initial set of groups, the one person that is contributing the most to the overall time, aka the "most unhappy person" (MUP) is determined. The algorithm then tries each of 4 basic moves. It starts by swapping the MUP with every other person that isn't in their group and checks to see if the total cost of the new set of groups is less than that for the existing set of groups. If the cost is lower, the new groups and their cost is saved. It then moves on and tries to add the MUP to the a group of 2, a group of 1, or a group of 0 (aka forms a new group). If at any time a better solution (lower cost) is found, the groupings and the cost replace the current best grouping/cost. Once every possible move for that individual is checked, a new MUP is determined and the process repeats. The search will stop if every person has had a chance to be the MUP and yet the cost has not decreased. This would mean that there is not a unilateral move that could improve the overall cost.

## Potential issues
Because the search gets called off after singular moves prove unfruitful, I have a feeling that the algorithm might get caught in a trap of a local minimum and never actually reach the global minimum. One potential thing to add would be a monte carlo element to purposefully choose worse states a small fraction of the time. Another potntial improvement would be to pick a more informed initial state as opposed to picking one randomly. For larger boards that can take a while to run, this might help shorten the length of time to find the solution. 




# References

[1] https://en.wikipedia.org/wiki/Haversine_formula  
[2] https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

