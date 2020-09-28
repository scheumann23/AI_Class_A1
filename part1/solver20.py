#!/usr/local/bin/python3
# solver20.py : 2020 Sliding tile puzzle solver
#
# Code by: Vishal Bhalla vibhalla, Neelan Scheumann nscheuma, Cody Harris harrcody
#
# Based on skeleton code by D. Crandall, September 2020
#
from queue import PriorityQueue
import sys

MOVES = { "R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1,0) }
ROWS = 4
COLS = 5

def valid_index(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS

# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row*COLS):(row*COLS+COLS)]
    return ( state[:(row*COLS)] + change_row[-dir:] + change_row[:-dir] + state[(row*COLS+COLS):], ("L" if dir == -1 else "R") + str(row+1) )

# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::COLS]
    s = list(state)
    s[col::COLS] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col+1) )

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

#one possible heuristic
def num_out_of_order(state):
    invs = [0 if state[i] == (i+1) else 1 for i in range(len(state))]
    return sum(invs)

#another possible heuristic
def num_inversions(state):
    invs = [0 if state[i+1] > state[i] else 1 for i in range(len(state)-1)]
    return sum(invs)

def manhattan(state):
    goal = sorted(state)
    state = list(state) 
    h2 = 0
    for i in range(1,len(state)+1):
        gl = goal.index(i)
        st = state.index(i)
        h2 += (abs(st%COLS - gl%COLS) + abs(st//COLS - gl//COLS))
    return h2

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
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    visited = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))