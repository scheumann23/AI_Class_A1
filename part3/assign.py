#!/usr/local/bin/python3
import numpy as np


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


def create_group_size_vector(prefs):
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


def total_grading_time(pairings, wants, dont_wants, group_size_pref, k, m, n):
    anti_pairings = (pairings * -1) + 1
    bad_pairs = np.trace(np.matmul(pairings, dont_wants.transpose()))
    missed_pairs = np.trace(np.matmul(anti_pairings, wants.transpose()))
    wrong_sizes = compare_group_sizes(group_size_pref, group_sizes(pairings))
    num_teams = count_of_teams(group_sizes(pairings))
    return (num_teams * k) + (bad_pairs * m) + (missed_pairs * n) + wrong_sizes
