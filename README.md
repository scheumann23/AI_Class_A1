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

This weight is retrieved by looking at the distance number for each segment in the road-segments.txt file.

### Time Edge Weight


