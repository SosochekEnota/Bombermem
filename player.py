from random import randint as rng

FIELD_SIZE = 19

map_matrix = [['#' if rng(0, 1) else '.' for _ in range(FIELD_SIZE)] for _ in range(FIELD_SIZE)]

for k in range(FIELD_SIZE):
    for l in range(FIELD_SIZE):
        if k % 2 == 0 and l % 2 == 0:
            map_matrix[k][l] = '*'

for k in range(4):
    for l in range(4):
        if k == 3 or l == 3:
            map_matrix[k][l], map_matrix[FIELD_SIZE - 1 - k][FIELD_SIZE - 1 - l] = '#', '#'
        else:
            map_matrix[k][l], map_matrix[FIELD_SIZE - 1 - k][FIELD_SIZE - 1 - l] = '.', '.'

for elem in map_matrix:
    elem[0], elem[-1] = '*', '*'

map_matrix[0], map_matrix[-1] = ['*' * FIELD_SIZE], ['*' * FIELD_SIZE]

map_matrix[1][1], map_matrix[FIELD_SIZE - 2][FIELD_SIZE - 2] = '1', '2'

file = open('map_2.txt', 'w+')
for elem in map_matrix:
    file.writelines(''.join(elem) + '\n')