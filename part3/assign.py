#!/usr/local/bin/python3
import numpy as np
import sys
import time

def load_data(file_name):
    data_list = []
    with open(file_name, 'r') as file:
        for line in file:
            line = line.strip('\n')
            data_list.append(list(line.split(' ')))
    return data_list

def create_initial_state(prefs):
    num_people = len(prefs)
    initial_state = np.ones((num_people, num_people))
    for row in range(num_people):
        for col in range(num_people):
            if  (col < ((row // 3)) * 3) or (col >= ((row // 3)+1) * 3):
                initial_state[row, col] = 0
    return initial_state

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

def group_size_vector(prefs):
    sizes = np.array([(group[1].count("-") + 1) for group in prefs])
    return sizes

def group_sizes(pairings):
    sizes = [sum(rows) for rows in pairings]
    return sizes

def compare_group_sizes(size1, size2):
    ls = []
    for i in range(len(size1)):
        if size1[i] == size2[i]:
            ls.append(0)
        else:
            ls.append(1)
    return np.array(ls)

def group_size_difs(size1, size2):
    ls = []
    for i in range(len(size1)):
        if size1[i] == size2[i]:
            ls.append(0)
        else:
            ls.append(1)
    return sum(ls)

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

def get_diag(matrix):
    ls = []
    for i in range(len(matrix)):
        ls.append(matrix[i][i])
    return np.array(ls)

def total_grading_time(pairings, wants, dont_wants, group_size_pref, k, m, n):
    anti_pairings = (pairings * -1) + 1
    bad_pairs = np.trace(np.matmul(pairings, dont_wants.transpose()))
    missed_pairs = np.trace(np.matmul(anti_pairings, wants.transpose()))
    wrong_sizes = group_size_difs(group_size_pref, group_sizes(pairings))
    num_teams = count_of_teams(group_sizes(pairings))
    return (num_teams * k) + (bad_pairs * m) + (missed_pairs * n) + wrong_sizes

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

def swap_people(pairings, p1, p2):
    new_pairings = np.copy(pairings)
    num_p = len(pairings)
    orig_pair_1_vec = pairings[p1]
    orig_pair_2_vec = pairings[p2]
    p1_vec = [1 if i == p1 else 0 for i in range(num_p)]
    p2_vec = [1 if i == p2 else 0 for i in range(num_p)]
    new_pair_1_vec = orig_pair_2_vec - p2_vec + p1_vec
    new_pair_2_vec = orig_pair_1_vec - p1_vec + p2_vec
    for i in range(num_p):
        if new_pair_1_vec[i] == 1:
            new_pairings[i] = new_pair_1_vec
    for i in range(num_p):
        if new_pair_2_vec[i] == 1:
            new_pairings[i] = new_pair_2_vec
    return new_pairings

def possible_moves_single(pairings, p1):
    groups = group_sizes(pairings)
    possible_places = [i for i in range(len(groups)) if groups[i] == 1 and i !=p1]
    return possible_places

def possible_moves_double(pairings, p1):
    groups = group_sizes(pairings)
    possible_places = [i for i in range(len(groups)) if groups[i] == 2 and i !=p1]
    return possible_places

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

def create_new_team(pairings, p1):
    new_pairings = np.copy(pairings)
    for rows in range(len(pairings)):
        if rows != p1:
            new_pairings[rows, p1] = 0
    for cols in range(len(pairings)):
        if cols != p1:
            new_pairings[p1, cols] = 0
    return new_pairings

def get_group_names(group_grid, labels):
    str_names = ''
    if type(group_grid) != 'numpy.ndarray':
        group_grid = np.array(group_grid)
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

def solve(pairings, wants, dont_wants, group_size_pref, k, m, n):
    unhappy_people = []
    all_people = list(range(len(pairings)))
    i = 0
    while set(unhappy_people) != set(all_people):
        cost = total_grading_time(pairings, wants, dont_wants, group_size_pref, k, m, n)
        initial_cost = cost
        most_unhappy_person = most_unhappy(pairings, wants, dont_wants, group_size_pref, k, m, n, unhappy_people)
        unhappy_person_vec = pairings[most_unhappy_person]
        possible_solution = pairings
        if i == 0:
            print(get_group_names(possible_solution,labels), int(cost))
        ## test all the possible swaps
        for i in range(len(pairings)):
            if unhappy_person_vec[i] == 0:
                new_pairings = swap_people(pairings, most_unhappy_person, i)
                if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
                    possible_solution = new_pairings
                    cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
                    print(get_group_names(possible_solution,labels), int(cost))
        ## try moving the person to a team of two
        for move in possible_moves_double(pairings, most_unhappy_person):
            new_pairings = move_person_double(pairings, most_unhappy_person, move)
            if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
                possible_solution = new_pairings
                cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
                print(get_group_names(possible_solution,labels), int(cost))
        ## try moving the person to a team of one
        for move in possible_moves_single(pairings, most_unhappy_person):
            new_pairings = move_person_single(pairings, most_unhappy_person, move)
            if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
                possible_solution = new_pairings
                cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
                print(get_group_names(possible_solution,labels), int(cost))
        ## try creating a new team (team of one) for this person
        new_pairings = create_new_team(pairings, most_unhappy_person)
        if total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n) < cost:
            possible_solution = new_pairings
            cost = total_grading_time(new_pairings, wants, dont_wants, group_size_pref, k, m, n)
            print(get_group_names(possible_solution,labels), int(cost))
        ## set up everything for the next loop
        if cost != initial_cost:
            unhappy_people = [most_unhappy_person]
        else:
            unhappy_people.append(most_unhappy_person)
        pairings = possible_solution
        i+=1


if __name__ == "__main__":
    data_file = sys.argv[1]
    k = int(sys.argv[2])
    m = int(sys.argv[3])
    n = int(sys.argv[4])

    data = load_data(data_file)

    labels = [people[0] for people in data]
    initial_state = create_initial_state(data)
    wants = create_want_matrix(data)
    dont_wants = create_dont_want_matrix(data)
    sizes = group_size_vector(data)

    print("Solving...")
    solve(initial_state, wants, dont_wants, sizes, k, m, n)
