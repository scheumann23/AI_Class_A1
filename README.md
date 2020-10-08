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


