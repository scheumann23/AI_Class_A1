import assign

labs = ['djcran', 'sahmaini', 'sulagaop', 'fanjun', 'nthakurd', 'vkvats']   
group =   [[1,0,0,0,1,1],
           [0,1,0,0,0,0],
           [0,0,1,1,0,0],
           [0,0,1,1,0,0],
           [1,0,0,0,1,1],
           [1,0,0,0,1,1]]
strings = get_group_names(group, labs)
print(strings)