# Part 1: The 2020 Puzzle

## Hueristics Evaluated

### Manhattan Distance

### Number out of Order

### Number of inversions

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


