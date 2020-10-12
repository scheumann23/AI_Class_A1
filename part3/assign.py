#!/usr/local/bin/python3
import numpy as np
import sys
import time

# Reads in the data from the external file and stores it in a list
def load_data(file_name):
    data_list = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            data_list.append(list(line.split(' ')))
    return data_list

# Creates a matrix (Numpy array) that represents an initial grouping of students. The matrix is structered such that for any 
# element (r,c) student r is in a group with student c if (r,c) is 1. If they aren't paired (r,c) is 0. Our initial board simply pairs up the students into groups of three
# starting with the first set of preferences in the data file and continues until all the students have been paired.
def create_initial_state(prefs):
    num_people = len(prefs)
    initial_state = np.ones((num_people, num_people))
    for row in range(num_people):
        for col in range(num_people):
            if  (col < ((row // 3)) * 3) or (col >= ((row // 3)+1) * 3):
                initial_state[row, col] = 0
    return initial_state

# This creates a matrix representation of the students that each student wants to work with. The element (r,c) will be 1
# if student r wants to work wth student c, else 0. Creating this matrix allows for a quick method to calculate the total
# cost of any grouping later on
def create_want_matrix(prefs):
    labels = [people[0] for people in prefs]
    total_list = []
    for i in range(len(labels)):
        want = prefs[i][1].split("-")
        ls = []
        for label in labels:
            if label in want:
                ls.append(1)
            else:
                ls.append(0)
        total_list.append(ls)
    want_matrix = np.array(total_list)
    return want_matrix

# This creates a matrix representation of the students that each student does not want to work with. The element (r,c) will 
# be 1 if student r does not want to work wth student c, else 0. Creating this matrix allows for a quick method to calculate 
# the total cost of any grouping later on
def create_dont_want_matrix(prefs):
    labels = [people[0] for people in prefs]
    total_list = []
    for i in range(len(labels)):
        want = prefs[i][2].split(",")
        ls = []
        for label in labels:
            if label in want:
                ls.append(1)
            else:
                ls.append(0)
        total_list.append(ls)
    dont_want_matrix = np.array(total_list)
    return dont_want_matrix

# This creates a vector to store the preffered number of students each student would like to have in their group. Once again,
# this will be utilzied in the total cost calcuation later
def group_size_vector(prefs):
    sizes = np.array([(group[1].count("-") + 1) for group in prefs])
    return sizes

# Given a potential set of groups (given in matrix form), this will calculate how many students are in each students group
def group_sizes(pairings):
    sizes = [sum(rows) for rows in pairings]
    return sizes

# This will return a list where the elements are either 0 if the elements of the two input lists at the same index are equal
# and 1 if they are different. This gets used when trying to see whch students have do not have their preferred group size
def compare_group_sizes(size1, size2):
    ls = []
    for i in range(len(size1)):
        if size1[i] == size2[i]:
            ls.append(0)
        else:
            ls.append(1)
    return np.array(ls)

# This is very similar to compare_group_sizes, but simply returns the total number of students that don't have their
# preferred group size. This is used as part of the total cost calc
def group_size_difs(size1, size2):
    ls = []
    for i in range(len(size1)):
        if size1[i] == size2[i]:
            ls.append(0)
        else:
            ls.append(1)
    return sum(ls)

# Calculate the number of teams given a set of team sizes. Since the sizes get repeated for each team member, each person in a
# team of 3 will have 3 people in their team, so if you count the number of 3's in the sizes vector and divide by 3
# that will tell you how many teams of three there are. The same can then be done for teams of two or one.
def count_of_teams(sizes):
    threes = 0 
    twos = 0
    ones = 0
    for size in sizes:
        if size == 3:
            threes += 1
        elif size == 2:
            twos += 1
        else:
            ones += 1
    return (threes / 3) + (twos / 2) + ones

# Simplay a function to return the diagonal elements of a matrix. This is needed for the most unhappy calc
def get_diag(matrix):
    ls = []
    for i in range(len(matrix)):
        ls.append(matrix[i][i])
    return np.array(ls)

# Calculates the total cost of a given set of student pairings. I utilize the matrices that were created earlier to quickly
# calculate both the number of people paired that don't want to be, and the number of people that aren't paired that did
# want to be. The formulas for bad_pairs and missed_pairs isn't intuitively obvious at first, but it works and should be
# very fast. 
def total_grading_time(pairings, wants, dont_wants, group_size_pref, k, m, n):
    anti_pairings = (pairings * -1) + 1
    #people that don't want to be paired
    bad_pairs = np.trace(np.matmul(pairings, dont_wants.transpose()))
    # people that aren't paired but wanted to be
    missed_pairs = np.trace(np.matmul(anti_pairings, wants.transpose()))
    # people that wanted a different group size than what they have. Compare the size vector calculated at the very beginning
    # and compare to the size vector calculated for this particular set of pairings
    wrong_sizes = group_size_difs(group_size_pref, group_sizes(pairings))
    # total number of teams
    num_teams = count_of_teams(group_sizes(pairings))
    #overall cost of this pairing
    return (num_teams * k) + (bad_pairs * m) + (missed_pairs * n) + wrong_sizes

# This is very similar to the total_grading_time calc, but instead of returning a single cost for a particular group, it 
# returns the student that has the highest individual cost (exlcuding the # of teams cost). This also takes in a list
# of people that have already been the "most unhappy person" and prevents a person from being the most unhappy two times in 
# a row. The reason this is necessary will become more clear when looking at the solve function.
def most_unhappy(pairings, wants, dont_wants, group_size_pref, k, m, n, unhappy_people):
    anti_pairings = (pairings * -1) + 1
    bad_pairs = get_diag(np.matmul(pairings, dont_wants.transpose()))
    missed_pairs = get_diag(np.matmul(anti_pairings, wants.transpose()))
    wrong_sizes = compare_group_sizes(group_size_pref, group_sizes(pairings))
    unhappy_dict = dict(enumerate((bad_pairs * m) + (missed_pairs * n) + wrong_sizes))
    
    for people in unhappy_people:
        del unhappy_dict[people]
    max_cost = -1
    max_index = 0
    for i, j in unhappy_dict.items():
        if j > max_cost:
            max_index = i
            max_cost = j
    return max_index

# This takes in a set of  pairings (again in matrix form) and returns a new matrix with students p1 and p2 on different teams
def swap_people(pairings, p1, p2):
    new_pairings = np.copy(pairings)
    num_p = len(pairings)
    orig_pair_1_vec = pairings[p1]
    orig_pair_2_vec = pairings[p2]
    p1_vec = [1 if i == p1 else 0 for i in range(num_p)]
    p2_vec = [1 if i == p2 else 0 for i in range(num_p)]
    # set the new rows of the matrix
    new_pair_1_vec = orig_pair_2_vec - p2_vec + p1_vec
    new_pair_2_vec = orig_pair_1_vec - p1_vec + p2_vec
    # so far only the p1, and p2 rows have been changed. We also need to change the rows for any student that was also on 
    # the same teams as p1 and p2. 
    #first fix the rows for everyone that was on p1's team
    for i in range(num_p):
        if new_pair_1_vec[i] == 1:
            new_pairings[i] = new_pair_1_vec
    #then fix the rows for everyone that was on p2's team
    for i in range(num_p):
        if new_pair_2_vec[i] == 1:
            new_pairings[i] = new_pair_2_vec
    return new_pairings

# determine which teams only have one person
def possible_moves_single(pairings, p1):
    groups = group_sizes(pairings)
    possible_places = [i for i in range(len(groups)) if groups[i] == 1 and i !=p1]
    return possible_places

# determine which teams only have two people
def possible_moves_double(pairings, p1):
    groups = group_sizes(pairings)
    possible_places = [i for i in range(len(groups)) if groups[i] == 2 and i !=p1]
    return possible_places

# move the person p1 onto a team t. Make sure to fix the row for the individual currently on team t as well
def move_person_single(pairings, p1, t):
    new_pairings = np.copy(pairings)
    for rows in range(len(pairings)):
        if rows == t:
            new_pairings[rows, p1] = 1
        elif rows != p1:
            new_pairings[rows, p1] = 0
    for cols in range(len(pairings)):
        if cols == t:
            new_pairings[p1, cols] = 1
        elif cols != p1:
            new_pairings[p1, cols] = 0
    return new_pairings

# Move student p1 onto team t (that has two people). Make sure to fix the rows for both students currently on team t
def move_person_double(pairings, p1, t):
    new_pairings = np.copy(pairings)
    t_team = pairings[t]
    members = [i for i in range(len(t_team)) if t_team[i] ==1]
    for rows in range(len(pairings)):
        if rows in members:
            new_pairings[rows, p1] = 1
        elif rows != p1:
            new_pairings[rows, p1] = 0
    for cols in range(len(pairings)):
        if cols in members:
            new_pairings[p1, cols] = 1
        elif cols != p1:
            new_pairings[p1, cols] = 0
    return new_pairings

# move a person to their own team. This essentially jsut zeros out the other elements in the row p1, and the column p1 that
# isn't (p1, p1)
def create_new_team(pairings, p1):
    new_pairings = np.copy(pairings)
    for rows in range(len(pairings)):
        if rows != p1:
            new_pairings[rows, p1] = 0
    for cols in range(len(pairings)):
        if cols != p1:
            new_pairings[p1, cols] = 0
    return new_pairings

# convert the set of pairings given as a matrix into human readable output
def get_group_names(group_grid, labels):
    str_names = ''
    if type(group_grid) != 'numpy.ndarray':
        group_grid = np.array(group_grid)
    #since each team will be repeated for each team member, we get rid of any duplicates
    unique_groups = np.unique(group_grid, axis = 0)
    name_index = [list(ind[0]) for ind in [np.where(team == 1) for team in unique_groups]]
    for name in name_index:
        for i, index in enumerate(name):
            if len(name) == i + 1:
                str_names += labels[index]
            else:
                str_names += labels[index] + '-'
        str_names += '\n'
    return str_names


# This is the meat of the whole program. It implements the search algorithm
def solve(pairings, wants, dont_wants, group_size_pref, k, m, n):
    # intitialize the list of unhappy people as an empty list
    unhappy_people = []
    # this is how we will know if each person has been the most unhappy person already
    all_people = list(range(len(pairings)))
    # a counter simply used to print the initial board in the first loop, but never again
    i = 0
    # As long as each person has not had a chance to be the most unhappy person, keep searching for a better solution
    while set(unhappy_people) != set(all_people):
        #calcuate the cost of the initial board
        cost = total_grading_time(pairings, wants, dont_wants, group_size_pref, k, m, n)
        # store the cost for later
        initial_cost = cost
        # determine the most unhappy person
        most_unhappy_person = most_unhappy(pairings, wants, dont_wants, group_size_pref, k, m, n, unhappy_people)
        # get the list of people in the most unhappy person's team 
        unhappy_person_vec = pairings[most_unhappy_person]
        # set the first possible soultion to the initial board
        possible_solution = pairings
        if i == 0:
            print(get_group_names(possible_solution,labels), int(cost))
        # Try swapping the most unhapy person with every other person that is not in their team
        for i in range(len(pairings)):
            if unhappy_person_vec[i] == 0:
                new_pairings = swap_people(pairings, most_unhappy_person, i)
                # if the new pairings happen to be better (aka lower cost) than the current one, set the new possible solution
                # and then store the new cost and print out the possible solution
                if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
                    possible_solution = new_pairings
                    cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
                    print(get_group_names(possible_solution,labels), int(cost))
        # try moving the MUP to each of the teams of two
        for move in possible_moves_double(pairings, most_unhappy_person):
            new_pairings = move_person_double(pairings, most_unhappy_person, move)
            # if the new pairings happen to be better (aka lower cost) than the current one, set the new possible solution
            # and then store the new cost and print out the possible solution
            if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
                possible_solution = new_pairings
                cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
                print(get_group_names(possible_solution,labels), int(cost))
        # try moving the MUP to each of the teams of one
        for move in possible_moves_single(pairings, most_unhappy_person):
            new_pairings = move_person_single(pairings, most_unhappy_person, move)
            # if the new pairings happen to be better (aka lower cost) than the current one, set the new possible solution
            # and then store the new cost and print out the possible solution
            if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
                possible_solution = new_pairings
                cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
                print(get_group_names(possible_solution,labels), int(cost))
        # try creating a new team (team of one) for the MUP
        new_pairings = create_new_team(pairings, most_unhappy_person)
        # if the new pairings happen to be better (aka lower cost) than the current one, set the new possible solution
        # and then store the new cost and print out the possible solution
        if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
            possible_solution = new_pairings
            cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
            print(get_group_names(possible_solution,labels), int(cost))
        # set up everything for the next loop
        # if the cost has changed, then reset the list of unhappy people otherwise, add the current MUP to the list
        if cost != initial_cost:
            unhappy_people = [most_unhappy_person]
        else:
            unhappy_people.append(most_unhappy_person)
        # set the pairings variable to the new possible_solution and then start all over again with a new MUP
        pairings = possible_solution
        i+=1


if __name__ == "__main__":
    data_file = sys.argv[1]
    k = int(sys.argv[2])
    m = int(sys.argv[3])
    n = int(sys.argv[4])

    # load the data
    data = load_data(data_file)

    # get a list of the students in the data set
    labels = [people[0] for people in data]
    #create the initial state
    initial_state = create_initial_state(data)
    #create the wants matrix
    wants = create_want_matrix(data)
    #create the don't want matrix
    dont_wants = create_dont_want_matrix(data)
    #create the size preference vector
    sizes = group_size_vector(data)

    print("Solving...")
    #Solve!
    solve(initial_state, wants, dont_wants, sizes, k, m, n)
